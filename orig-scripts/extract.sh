#!/usr/bin/bash

cd Downloads
unxz linux-"$1".tar.xz
tar -xvf linux-"$1".tar

current_user=$(whoami)
chown -R "$current_user:$current_user" linux-"$1"

#	Remove the tar file so recover a smidgen of space
rm linux-"$1".tar
