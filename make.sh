#!/usr/bin/bash

cd Downloads/linux-"$1"
make -j2 ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- all

if [ ! -d ../../build/linux-"$1"-bpi-gurumode ]; then
	mkdir ../../build/linux-"$1"-bpi-gurumode
fi

make ARCH=arm64 INSTALL_MOD_PATH=../../build/linux-"$1"-bpi-gurumode modules_install

mv arch/arm64/boot/Image ../../build/linux-"$1"-bpi-gurumode/Image
mv System.map ../../build/linux-"$1"-bpi-gurumode/
mv .config ../../build/linux-"$1"-bpi-gurumode/
