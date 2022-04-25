# Nibe MQTT integration
MQTT integration for controlling Nibe heatpumps. Supports HomeAssistant MQTT Autodiscovery.

Uses [nibe](https://github.com/yozik04/nibe) library which initially supports only RS485 communication via NibeGW developed by Pauli Anttila for [Openhab's integration](https://www.openhab.org/addons/bindings/nibeheatpump/).

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

## Basic configuration

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
```

For all configuration options lookup in config.py