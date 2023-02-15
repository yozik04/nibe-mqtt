from nibe_mqtt.config import schema

def test_nibegw():
    config = schema(
        {
            "mqtt": {"host": "192.168.1.2"},
            "nibe": {
                "nibegw": {"ip": "192.168.1.3"},
                "model": "F1255",
                "poll": {"coils": ["bt50-room-temp-s1-40033", 40033]},
            },
        }
    )

    assert "modbus" not in config["nibe"]
    assert config["nibe"]["poll"]["interval"] == 60

    print(config)

def test_modbus():
    config = schema(
        {
            "mqtt": {"host": "192.168.1.2"},
            "nibe": {
                "modbus": {"url": "tcp://127.0.0.1:502", "slave_id": 1},
                "model": "F1255",
                "poll": {"coils": ["bt50-room-temp-s1-40033", 40033]},
            },
        }
    )

    assert "nibegw" not in config["nibe"]
    assert config["nibe"]["poll"]["interval"] == 60

    print(config)
