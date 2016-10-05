#!/bin/bash

# run as root

# BIOS:
# - enable VT-d (can be verified from `dmesg|grep -e DMAR -e IOMMU`)

# Kernel boot command:
# iommu=pt intel_iommu=on 

# persistent allocation of huge pages
echo 'vm.nr_hugepages=2048' > /etc/sysctl.d/hugepages.conf

# mount huge pages
mount -t hugetlbfs none /dev/hugepages 

# setup kernel modules
modprobe uio 
insmod $DPDK_DIR/x86_64-native-linuxapp-gcc/kmod/igb_uio.ko


