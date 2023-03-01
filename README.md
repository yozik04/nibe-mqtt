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

## Installation
### PyPi
It is possible to install directly from PyPi
```bash
pip3 install nibe-mqtt
```

Then you will be able to run the service with command
```bash
nibe-mqtt -c config.yaml
```

### Docker
See [Docker Hub](https://hub.docker.com/repository/docker/yozik04/nibe-mqtt) for available versions (tags)

Run with:
```bash
docker run -ti --pull=always --rm -p 9999:9999/udp -v "/Users/myuser/Desktop/config.yaml:/config/nibe-mqtt/config.yaml:ro" yozik04/nibe-mqtt:latest
```

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
  word_swap: true
  modbus:
    url: tcp://192.168.1.3:502
    slave_id: 1
  poll:
    coils:
      - bt50-room-temp-s1-40033
```

For all configuration options lookup in config.py

## Supported coils
See the list of available parameters [here](https://github.com/yozik04/nibe/tree/master/nibe/data)

## Writing Registers
See the list of supported coils to find out which registers can be written (set). For setting a register/coil, publish your data under the following topic: `[prefix]/[coil]/set`. Example: Publish `ONE TIME INCREASE` to `nibe/coils/temporary-lux-48132/set` for turning on temporary hot water lux mode.

## Word swap
You might need to specify `word_swap` setting to let underneath library understand how to decode 32-bit integers (mostly counters). For most of the heat pumps with NibeGW connection method it will be auto detected (since `nibe-mqtt 1.1.0`, `nibe 2.1.0`).

```yaml
...
nibe:
  ...
  word_swap: true
  ...
```

You can find the setting value in you Heat pump service menu 5.3.11 (`modbus settings`), there is a setting called `word swap`.

You need to set `word_swap` setting in yaml to match the setting in the service menu.

Failing to do so will start throwing errors with decoding errors of 32-bit registers.

## Disclaimer
Nibe is registered mark of NIBE Energy Systems.

The code was developed as a way of integrating personally owned Nibe heatpump, and it cannot be used for other purposes. It is not affiliated with any company, and it doesn't have a commercial intent.

The code is provided AS IS and the developers will not be held responsible for failures in the heatpump operation or any other malfunction.
