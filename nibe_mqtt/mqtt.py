import asyncio
import json
import logging
import os
from abc import ABC, abstractmethod
from typing import Union

from nibe.coil import Coil
from paho.mqtt.client import Client, MQTTMessage

logger = logging.getLogger("nibe").getChild(__name__)


class MqttHandler(ABC):
    @abstractmethod
    def handle_coil_set(self, name, value):
        pass


class MqttConnection:
    def __init__(self, handler: MqttHandler, conf: dict):
        self._loop = asyncio.get_event_loop()
        self._conf = conf
        self._handler = handler

        self._availability_topic = f"{conf['prefix']}/availability"

        self._client = Client(
            "nibe" + os.urandom(8).hex(),
            protocol=conf["protocol"],
            transport="tcp",
        )

        if conf.get("username"):
            self._client.username_pw_set(
                username=conf["username"], password=conf["password"]
            )

        self._client.will_set(
            self._availability_topic, "offline", retain=conf["retain_availability"]
        )

        self._client.on_connect = self._on_connect_cb
        self._client.on_disconnect = self._on_disconnect_cb
        self._client.on_message = self._on_message_cb

    def _on_connect_cb(self, client, userdata, flags, result, properties=None):
        logger.warning("MQTT connected")

        self._client.publish(
            self._availability_topic, "online", retain=self._conf["retain_availability"]
        )
        self._client.subscribe(f"{self._conf['prefix']}/coils/+/set")

    def _on_disconnect_cb(self, client, userdata, rc, properties=None):
        logger.warning("MQTT disconnected")

    def _on_message_cb(self, client, userdata, msg: MQTTMessage):
        coil_name = msg.topic.removeprefix(self._conf["prefix"]).split("/")[2]
        value = msg.payload.decode("utf-8")
        value = _try_cast_to_numeric(value)

        logger.info(f"Received MQTT command set {coil_name} to {value}")

        self._loop.call_soon_threadsafe(self._handler.handle_coil_set, coil_name, value)

    def start(self):
        self._client.connect_async(host=self._conf["host"], port=self._conf["port"])

        self._client.loop_start()

    def stop(self):
        self._client.loop_stop()

    def _get_coil_state_topic(self, coil: Coil):
        return f"{self._conf['prefix']}/coils/{coil.name}"

    def publish_coil_state(self, coil: Coil):
        self._client.publish(
            self._get_coil_state_topic(coil),
            coil.value,
            retain=self._conf["retain_state"],
        )

    def publish_discovery(self, coil: Coil, device_info: dict):
        component = "sensor"

        device_id = device_info.get("id")
        device = {
            "manufacturer": "Nibe",
            "name": device_info.get("name"),
            "model": device_info.get("model"),
            "identifiers": [device_id],
            # "sw_version": ""
        }

        unique_id = f"{device_id}_{coil.name}"
        config = {
            "name": coil.title,
            "unique_id": unique_id,
            "object_id": unique_id,
            "state_topic": self._get_coil_state_topic(coil),
            "availability_topic": self._availability_topic,
            "device": device,
        }
        uom = coil.unit
        if uom is not None:
            config["unit_of_measurement"] = uom
            if uom == "°C":
                config["device_class"] = "temperature"
                config["state_class"] = "measurement"
            elif uom in ["h", "min"]:
                config["device_class"] = "duration"
            elif uom in ["kW", "W"]:
                config["device_class"] = "power"
            elif uom == "kWh":
                config["device_class"] = "energy"
            elif uom == "Hz":
                config["device_class"] = "frequency"
        if coil.is_boolean:
            if coil.is_writable:  # switch
                component = "switch"
                config["command_topic"] = f"{config['state_topic']}/set"
            else:  # binary_sensor
                component = "binary_sensor"
        elif coil.is_writable:  # switch
            if coil.mappings:
                component = "select"
                config["command_topic"] = f"{config['state_topic']}/set"
                config["options"] = list(coil.reverse_mappings.keys())
            else:
                component = "number"
                config["command_topic"] = f"{config['state_topic']}/set"
                config["min"] = coil.min
                config["max"] = coil.max
                config["step"] = 1 / coil.factor

        self._client.publish(
            f"{self._conf['discovery_prefix']}/{component}/{device_id}/{coil.name}/config",
            json.dumps(config),
            retain=self._conf["retain_state"],
        )


def _try_cast_to_numeric(value) -> Union[str, int, float]:
    try:
        return int(value)
    except ValueError:
        pass

    try:
        return float(value)
    except ValueError:
        pass

    return value
