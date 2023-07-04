# kernel-get
Download, compile, and package the latest rolling stable Linux kernel.  This is geared for Arch running on Banana Pi R3 router board, but could be adapted to other systems.

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
