#!/bin/bash

BASE_DIR=/opt/nfvacc
DPDK_DIR=$BASE_DIR/dpdk-16.07
DPDK_TARGET=x86_64-native-linuxapp-gcc
DPDK_BUILD=$DPDK_DIR/$DPDK_TARGET
OVS_VERSION=2.6.0
OVS_DIR=$BASE_DIR/openvswitch-${OVS_VERSION}
OVS_RUNDIR=$BASE_DIR/openvswitch-${OVS_VERSION}-runtime
OVS_DB_SOCK=$OVS_RUN_DIR/var/run/openvswitch/db.sock
SLEEP_SECS=1
