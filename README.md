# Nibe MQTT integration
MQTT integration for controlling Nibe heatpumps. Supports HomeAssistant MQTT Autodiscovery.

Uses [nibe](https://github.com/yozik04/nibe) library which supports connections:
  - RS485 communication via NibeGW developed by Pauli Anttila for [Openhab's integration](https://www.openhab.org/addons/bindings/nibeheatpump/)
  - TCP/Serial Modbus (experimental)

#### Supported heatpump models
 - F1145
 - F1155
 - F1245
 - F1255
 - F1345
 - F1355
 - F370
 - F470
 - F730
 - F750
 - SMO20
 - SMO40
 - VVM225
 - VVM310
 - VVM320
 - VVM325
 - VVM500

Additionally, supports some S series through TCP Modbus (experimental)

## Basic configuration

### With NibeGW:
```yaml
mqtt:
  host: 192.168.1.2
  protocol: 5
  username: user
  password: pass
nibe:
  model: F1255
  nibegw:
    ip: 192.168.1.3
  poll:
    coils:
      - bt50-room-temp-s1-40033
```

For all configuration options lookup in config.py

### With Modbus:
```yaml
mqtt:
  host: 192.168.1.2
  protocol: 5
  username: user
  password: pass
nibe:
  model: F1255
  modbus:
    url: tcp://192.168.1.3:502
    slave_id: 1
  poll:
    coils:
      - bt50-room-temp-s1-40033
```

For all configuration options lookup in config.py

## Disclaimer
Nibe is registered mark of NIBE Energy Systems.

The code was developed as a way of integrating personally owned Nibe heatpump, and it cannot be used for other purposes. It is not affiliated with any company, and it doesn't have a commercial intent.

The code is provided AS IS and the developers will not be held responsible for failures in the heatpump operation or any other malfunction.
