import asyncio
import logging
from pathlib import Path
from slugify import slugify

from nibe.coil import Coil
from nibe.connection.nibegw import NibeGW
from nibe.exceptions import CoilWriteException
from nibe.heatpump import HeatPump

from nibe_mqtt import cfg
from nibe_mqtt.mqtt import MqttConnection, MqttHandler

logger = logging.getLogger("nibe").getChild(__name__)


class Service(MqttHandler):
    def __init__(self, conf):
        self.conf = conf
        self.heatpump = HeatPump(conf['nibe']['model'])
        self.heatpump.initialize()
        self.announced_coils = set()

        self.heatpump.subscribe(HeatPump.COIL_UPDATE_EVENT, self.on_coil_update)

        self.connection = NibeGW(
            heatpump=self.heatpump,
            remote_ip=conf['nibe']['nibegw']['ip'],
            remote_read_port=conf['nibe']['nibegw']['read_port'],
            remote_write_port=conf['nibe']['nibegw']['write_port'],
        )

        self.mqtt_client = MqttConnection(self, conf['mqtt'])

    def _get_device_info(self) -> dict:
        return {
            "model": self.conf['nibe']['model'].name,
            "name": "Nibe heatpump integration",
            "id": slugify("Nibe " + self.conf['nibe']['nibegw']['ip'])
        }

    def handle_coil_set(self, name, value):
        coil = self.heatpump.get_coil_by_name(name)
        try:
            coil.value = value

            asyncio.create_task(self._write_coil(coil))
        except AssertionError as e:
            logger.error(e)
        except Exception as e:
            logger.exception("Unhandled exception", e)

    async def _write_coil(self, coil):
        try:
            await self.connection.write_coil(coil)
        except CoilWriteException as e:
            logger.error(e)
        except Exception as e:
            logger.exception("Unhandled exception", e)

    async def start(self):
        await self.connection.start()

        self.mqtt_client.start()

    def on_coil_update(self, coil: Coil):
        if coil not in self.announced_coils:
            self.mqtt_client.publish_discovery(coil, self._get_device_info())
            self.announced_coils.add(coil)

        self.mqtt_client.publish_coil_state(coil)


if __name__ == "__main__":
    conf = cfg.load(Path('config.yaml'))

    service = Service(conf)

    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(service.start())
    loop.run_forever()
