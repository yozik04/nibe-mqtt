
from unittest import mock

import pytest

from nibe.coil import CoilData

from nibe_mqtt.config import schema
from nibe_mqtt.service import Service


@pytest.fixture
def nibegw_config():
    return schema({
        "mqtt": {"host": "127.0.0.1"},
        "nibe": {
            "nibegw": {"ip": "127.0.0.1"},
            "model": "F1255"
        },
    })

@pytest.fixture
def modbus_config():
    return schema({
        "mqtt": {"host": "127.0.0.1"},
        "nibe": {
            "modbus": {"url": "tcp://127.0.0.1:502", "slave_id": 1},
            "model": "S2125"
        },
    })

@pytest.fixture(name="nibegw_connection", autouse=True)
def nibegw_connection():
    from nibe.connection.nibegw import NibeGW
    return mock.Mock(spec=NibeGW)


@pytest.fixture(name="modbus_connection", autouse=True)
def modbus_connection():
    from nibe.connection.modbus import Modbus
    return mock.Mock(spec=Modbus)


@pytest.fixture(name="mqtt_connection", autouse=True)
def mqtt_connection():
    from nibe_mqtt.mqtt import MqttConnection
    return mock.Mock(spec=MqttConnection)


async def test_service_nibegw(nibegw_config):
    service = Service(nibegw_config)

    await service.start()

    assert len(service.heatpump.get_coils()) > 0

    outdoor_temperature = service.heatpump.get_coil_by_address(40004)
    coil_data = CoilData(outdoor_temperature, 10)
    service.on_coil_update(coil_data)


async def test_service_modbus(modbus_config):
    service = Service(modbus_config)

    await service.start()

    assert len(service.heatpump.get_coils()) > 0

    outdoor_temperature = service.heatpump.get_coil_by_address(30002)
    coil_data = CoilData(outdoor_temperature, 10)
    service.on_coil_update(coil_data)
