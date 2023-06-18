#!/usr/bin/bash

cd Downloads/linux-"$1"
make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- all
