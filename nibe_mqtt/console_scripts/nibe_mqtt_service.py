#!/usr/bin/env python3
import argparse
import asyncio
import logging
import sys
from pathlib import Path

from nibe_mqtt import cfg, __version__ as nibe_mqtt_version
from nibe_mqtt.service import Service
from nibe import __version__ as nibe_lib_version

if sys.version_info < (
    3,
    9,
):
    print(
        "You are using Python %s.%s, but Nibe daemon requires at least Python 3.9"
        % (sys.version_info[0], sys.version_info[1])
    )
    sys.exit(-1)


def main():
    args = parse_arguments()
    conf = cfg.load(Path(args.config))

    service = Service(conf)

    logging.basicConfig(**conf["logging"])

    logging.info(f"Running Nibe MQTT {nibe_mqtt_version} service with Nibe {nibe_lib_version} lib")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(service.start())
    loop.run_forever()


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        default="config.yaml",
        help="specify path to a configuration file",
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
