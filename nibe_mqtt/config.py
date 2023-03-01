import ipaddress
from pathlib import Path

import yaml
from nibe.heatpump import Model
from paho.mqtt.client import MQTTv5, MQTTv31, MQTTv311
from voluptuous import (All, Any, Exclusive, Inclusive, InInvalid, Optional, Range,
                        Required, Schema, ValueInvalid,)

mqtt_protocol_map = {"3.1": MQTTv31, "3.1.1": MQTTv311, "5": MQTTv5}


port = All(int, Range(min=1024, max=65535))


def ip_address(v):
    try:
        ipaddress.ip_address(v)
    except ValueError as e:
        raise ValueInvalid(str(e))
    return v


def heatpump_model(key: str):
    try:
        return getattr(Model, key)
    except AttributeError:
        raise InInvalid(f"'{key}' not in {Model.keys()}")


def mqtt_protocol(key: str):
    try:
        return mqtt_protocol_map[str(key)]
    except KeyError:
        raise InInvalid(f"'{key}' not in {mqtt_protocol_map.keys()}")


nibe_schema = Schema(
    {
        Exclusive("nibegw", "connection"): {
            Optional("listening_ip", default="0.0.0.0"): ip_address,
            Optional("listening_port", default=9999): port,
            Required("ip"): ip_address,
            Optional("read_port", default=9999): port,
            Optional("write_port", default=10000): port,
        },
        Exclusive("modbus", "connection"): {
            Required("url"): str,
            Required("slave_id"): int,
            Optional("options", default=None): Any(None, dict),
        },
        Required("model"): heatpump_model,
        Optional("word_swap", default=None): Any(None, bool),
        Optional("poll"): {
            Optional("interval", default=60): All(int, Range(min=5, max=60 * 60 * 24)),
            Optional("coils"): [str, int],
        }
    }
)

schema = Schema(
    {
        Required("mqtt"): {
            Optional("discovery_prefix", default="homeassistant"): str,
            Optional("prefix", default="nibe"): str,
            Required("host"): str,
            Optional("port", default=1883): port,
            Inclusive("username", "auth"): str,
            Inclusive("password", "auth"): str,
            Optional("protocol", default="3.1.1"): mqtt_protocol,
            Optional("retain_state", default=True): bool,
            Optional("retain_availability", default=True): bool,
        },
        Required("nibe"): nibe_schema,
        Optional("logging", default={}): {
            Optional("level", default="INFO"): str,
            Optional(
                "format", default="%(asctime)s - %(levelname)-8s - %(message)s"
            ): str,
        },
    }
)


class Config:
    def __init__(self):
        self._data = None

    def load(self, config_file: Path) -> dict:
        assert config_file.is_file(), f"{config_file} should be a file"
        with config_file.open("r", encoding="utf-8") as fh:
            self._data = schema(yaml.safe_load(fh))

        return self._data

    def get(self):
        assert self._data is not None, "Not yet loaded"

        return self._data
