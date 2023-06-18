#!/usr/bin/bash

cd Downloads/linux-"$1"
make mrproper

cp ../../kernel.config .config
