#!/bin/bash

export BASE_DIR=/opt/nfvacc
export DPDK_DIR=$BASE_DIR/dpdk-16.07
export DPDK_TARGET=x86_64-native-linuxapp-gcc
export DPDK_BUILD=$DPDK_DIR/$DPDK_TARGET
export OVS_VERSION=2.6.0
export OVS_DIR=$BASE_DIR/openvswitch-${OVS_VERSION}
export OVSDB_SCHEMA=$OVS_DIR/vswitchd/vswitch.ovsschema 

#OVSDB_RUN_DIR=$BASE_DIR/openvswitch-${OVS_VERSION}-runtime
export OVSDB_RUN_DIR=/usr/local/

export OVS_RUN_DIR=/usr/local/var/run/openvswitch/
export OVS_ETC_DIR=/usr/local/etc/openvswitch/
export OVS_LOG_DIR=/usr/local/var/log/openvswitch/

export OVSDB_SOCK=$OVS_RUN_DIR/db.sock
export OVSDB_CONF=$OVS_ETC_DIR/conf.db
export OVSDB_LOG_FILE=$OVS_LOG_DIR/ovsdb-server.log
export OVSDB_PID_FILE=$OVS_RUN_DIR/ovsdb-server.pid
export OVS_VHOST_SUBDIR=vhost-sock

export SLEEP_SECS=1
