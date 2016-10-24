## Creating a base image with packer

1.  Download packer binary to your home (https://www.packer.io/docs/installation.html)
2.  Invoke packer:

```bash
mkdir ~/packer_cache
export PACKER_CACHE_DIR=~/packer_cache
~/packer build ubuntu-14.04-server-amd64.json
```

The following command is being executed in the background: 

```bash
qemu-system-x86_64 -vnc 0.0.0.0:92 -name packer-ubuntu-1404-server -netdev user,id=user.0,hostfwd=tcp::3789-:22 -device virtio-net,netdev=user.0 -boot once=d -machine type=pc,accel=kvm -display sdl -drive file=out/packer-ubuntu-1404-server,if=virtio,cache=writeback,discard=ignore -cdrom /home/nanastop/nfv-stress/vnfs/packer/ubuntu_1404_server/packer_cache/f8fd5c3ff54d2ced0eca03e93f30f0f53477156699278433e327e4e3d6752ff8.iso
-m 512M
```

3. Launch QEMU instance:

```
qemu-system-x86_64 -machine type=pc,accel=kvm -device virtio-net,netdev=user.0 -m 512M  -name ubuntu_14_04_server -netdev user,id=user.0,hostfwd=tcp::3213-:22 -drive file=./out/packer-ubuntu-1404-server,if=virtio,cache=writeback,discard=ignore
```
