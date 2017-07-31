set -eux
#./dpdk_install
#./ovdk_install
#./qemu_install

./ovdk_stop
./dpdk_unload_modules
./dpdk_unmount_huge

./dpdk_load_modules
./dpdk_mount_huge
./dpdk_bind_status
./dpdk_bind_ifaces --interfaces 0000:03:00.0,0000:03:00.1
./dpdk_bind_status

./ovdk_start --dpdk-lcore-mask f --dpdk-pmd-mask f
./ovdk_show
./ovdk_br_add --bridge fastbr0
./ovdk_br_show --bridge fastbr0
./ovdk_dpdkport_add --bridge fastbr0 --port dev1 --pci-addr 0000:03:00.0
./ovdk_dpdkport_add --bridge fastbr0 --port dev2 --pci-addr 0000:03:00.1 
#./ovdk_dpdkport_add --bridge fastbr0 --port dev2 --pci-addr 0000:03:00.1 --rx-queues 2 --rx-size 1024 --rx-aff "0:0,1:2" --tx-queues 2 --tx-size 1024 --tx-aff "0:3,1:5"
./ovdk_br_show --bridge fastbr0
./ovdk_vhostport_add --bridge fastbr0 --port vhost-user1
./ovdk_vhostport_add --bridge fastbr0 --port vhost-user2

#  ./qemu_start_vhostuser --cpu-list 0,1 --name foo --enable-kvm --guest-mem 8192M --nsockets 1 --qcow2-image /store/images/nanastop/dpdk-test.root.img --cores-per-socket 4 --interfaces '[{"port":"vhost-user1","queues":2},{"port":"vhost-user2","queues":2}]' --cloud-init-config /store/images/nanastop/dpdk-test.configuration.iso
