# nfv-stress

## Steps

```
cd scripts
./dpdk_install
./ovdk_install
./qemu_install

./dpdk_unload_modules
./dpdk_load_modules
./dpdk_unmount_huge
./dpdk_mount_huge
./dpdk_bind_status
./dpdk_bind_ifaces --interfaces 0000:03:00.0,0000:03:00.1
./dpdk_bind_status

```

## Root privileges
- load/unload modules: insmod, modprobe, rmmod
- mount/umount huge memory pages: mount, umount
- bind/unbind interfaces: for this we need recursive rw access to:
   - `/sys/bus/pci/devices/0000:01:00.0`
   - `/sys/bus/pci/devices/0000:01:00.1`
   - `/sys/bus/pci/drivers/igb/`
   - `/sys/bus/pci/drivers/igb_uio/`
   - `/sys/bus/pci/drivers/ixgbe/`
- read-write access for OVSDB:
   - /usr/local/var/run/openvswitch/
   - /usr/local/var/log/openvswitch/
   - /usr/local/etc/openvswitch/
- read-write access to /var/run in order to create /var/run/openvswitch

## TODO
