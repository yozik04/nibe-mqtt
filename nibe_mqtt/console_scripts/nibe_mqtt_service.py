#!/usr/bin/env python3
from __future__ import annotations

import argparse
import asyncio
import sys

from nibe import __version__ as nibe_lib_version

from nibe_mqtt import __version__ as nibe_mqtt_version
from nibe_mqtt.service import run_service

if sys.version_info < (3, 9):
    print(f"You are using Python {sys.version_info[0]}.{sys.version_info[1]}, but Nibe daemon requires at least Python 3.9")
    sys.exit(-1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", type=str, default="config.yaml", help="specify path to a configuration file")
    args = parser.parse_args()

    version_msg = f"Running Nibe MQTT {nibe_mqtt_version} service with Nibe {nibe_lib_version} lib"
    asyncio.run(run_service(args.config, log_version=version_msg))


if __name__ == "__main__":
    main()
