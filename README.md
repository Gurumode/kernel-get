# kernel-get
Download and compile the newest Linux kernel.

# dependencies

kernel-get has only been tested on Arch.  The initial purpose for this is to build a kernel for Arch on Banana Pi R3 router board.  With that in mind:

```
pacman -S base-devel
pacman -S python
pacman -S python-beautifulsoup4
pacman -S python-requests
```

# running

```
python check-release.py
```

This will check for the latest kernel release, download and compile it.
