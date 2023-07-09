# kernel-get
Download, compile, and package the latest rolling stable Linux kernel.  This is geared for Arch running on Banana Pi R3 router board, but could be adapted to other systems.

# using gurumode kernel

If you would like to use the kernel without compiling you are in luck.  Just add the repo and install!

Add the bpir64-gurumode repo to /etc/pacman.conf if you have not already

```
[bpir64-gurumode]
Server = http://repo.gurumode.net/bpir64-gurumode
```

You will also need to add the repo key and sign it locally.

```
# Download and add the key
wget http://repo.gurumode.net/bpir64-gurumode/bpir64-gurumode.asc
sudo pacman-key --add bpir64-gurumode.asc
pacman-key --finger B0401A392442717F9D23341894BFC66AEAF875B0

# Locally sign the key, and update package information
sudo pacman-key --lsign-key B0401A392442717F9D23341894BFC66AEAF875B0
sudo pacman -Sy
```

Finally, to install the kernel and kernel headers

```
sudo pacman -S linux-bpir64-gurumode
sudo pacman -S linux-bpir64-gurumode-headers
```

## kernel compilation

# dependencies

kernel-get has only been tested on Arch.  With that in mind:

```
pacman -S base-devel
pacman -S python
pacman -S python-beautifulsoup4
pacman -S python-requests
pacman -S python-lxml
```

# running

```
python check-release.py
```

This will check for the latest kernel release, download and compile it.  It will then be packaged for installation with Pacman.
