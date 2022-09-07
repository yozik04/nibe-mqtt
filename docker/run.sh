#!/bin/sh

set -e

CONF_DIR="/config/nibe-mqtt"
if [ ! -f "$CONF_DIR/config.yaml" ]; then
  mkdir -p "$CONF_DIR"
  cp "/default/config_example.yaml" "$CONF_DIR/config.yaml"
fi

nibe-mqtt -c "$CONF_DIR/config.yaml"