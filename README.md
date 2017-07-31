# dputils



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
