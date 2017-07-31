set -eux

# Install software
#./dpdk_install
#./ovdk_install
#./qemu_install

# Clean from previous runs
./ovdk_stop
./dpdk_unload_modules
./dpdk_unmount_huge

# Prepare DPDK environment 
./dpdk_load_modules
./dpdk_mount_huge

# Bind physical interfaces to DPDK (bypass if OVS is intended for inter-VM traffic only)
./dpdk_bind_status
./dpdk_bind_ifaces --interfaces 0000:03:00.0,0000:03:00.1
./dpdk_bind_status

# Start OVS
./ovdk_start --dpdk-lcore-mask f --dpdk-pmd-mask f
./ovdk_show

# Create bridge on OVS
./ovdk_br_add --bridge fastbr0
./ovdk_br_show --bridge fastbr0

# Add physical DPDK interfaces as ports to bridge (bypass if inter-VM traffic only)
./ovdk_dpdkport_add --bridge fastbr0 --port dev1 --pci-addr 0000:03:00.0
./ovdk_dpdkport_add --bridge fastbr0 --port dev2 --pci-addr 0000:03:00.1 
# More elaborate port configuration
#./ovdk_dpdkport_add --bridge fastbr0 --port dev2 --pci-addr 0000:03:00.1 --rx-queues 2 --rx-size 1024 --rx-aff "0:0,1:2" --tx-queues 2 --tx-size 1024 --tx-aff "0:3,1:5"
./ovdk_br_show --bridge fastbr0

# Add vhost ports to bridge
./ovdk_vhostport_add --bridge fastbr0 --port vhost-user1
./ovdk_vhostport_add --bridge fastbr0 --port vhost-user2

# Start QEMU instance with 2 interfaces, each bound on vhost-user1, vhost-user2 ports, respectively
 ./qemu_start_vhostuser --cpu-list 0,1 --name foo --enable-kvm --guest-mem 8192M --nsockets 1 --cores-per-socket 4 \
      --qcow2-image /store/images/nanastop/dpdk-test.root.img \
      --cloud-init-config /store/images/nanastop/dpdk-test.configuration.iso \
      --interfaces '[{"port":"vhost-user1","queues":2},{"port":"vhost-user2","queues":2}]' 
      
