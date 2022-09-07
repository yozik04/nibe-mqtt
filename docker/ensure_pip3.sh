#!/bin/sh

if hash pip3 2>/dev/null; then
    echo "Python exists"
    exit 0
fi

if hash apk 2>/dev/null; then
    echo "Installing python with apk"
    apk add --no-cache python3 py3-pip
fi

if hash apt 2>/dev/null; then
    echo "Installing python with apt"
    apt-get -y update
    apt-get install -y python3 python3-pip
    rm -rf /var/lib/apt/lists/*
fi