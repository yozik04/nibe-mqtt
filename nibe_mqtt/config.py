from pathlib import Path

import yaml
from paho.mqtt.client import MQTTv31, MQTTv311, MQTTv5
from voluptuous import Schema, Required, Optional, Inclusive, In, InInvalid, Range, Exclusive

from nibe.heatpump import Model

mqtt_protocol_map = {
    "3.1": MQTTv31,
    "3.1.1": MQTTv311,
    "5": MQTTv5
}


port = Range(min=1024, max=65535)


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


nibe_schema = Schema({
    Exclusive('nibegw', 'connection'): {
        Optional('local_port', default=9999): port,
        Required('ip'): str,
        Optional('read_port', default=9999): port,
        Optional('write_port', default=10000): port,
    },
    Required('model'): heatpump_model
})

schema = Schema({
    Required('mqtt'): {
        Optional('discovery_prefix', default='homeassistant'): str,
        Optional('prefix', default='nibe'): str,
        Required('host'): str,
        Optional('port', default=1883): port,
        Inclusive('username', 'auth'): str,
        Inclusive('password', 'auth'): str,
        Optional('protocol', default='3.1.1'): mqtt_protocol,
        Optional('retain_state', default=True): bool,
        Optional('retain_availability', default=True): bool
    },
    Required('nibe'): nibe_schema
})


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