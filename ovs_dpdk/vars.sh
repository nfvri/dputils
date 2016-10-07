#!/bin/bash

BASE_DIR=/opt/nfvacc
DPDK_DIR=$BASE_DIR/dpdk-16.07
DPDK_TARGET=x86_64-native-linuxapp-gcc
DPDK_BUILD=$DPDK_DIR/$DPDK_TARGET
OVS_VERSION=2.6.0
OVS_DIR=$BASE_DIR/openvswitch-${OVS_VERSION}
OVSDB_SCHEMA=$OVS_DIR/vswitchd/vswitch.ovsschema 

#OVSDB_RUN_DIR=$BASE_DIR/openvswitch-${OVS_VERSION}-runtime
OVSDB_RUN_DIR=/usr/local/

OVS_RUN_DIR=/usr/local/var/run/openvswitch/
OVS_ETC_DIR=/usr/local/etc/openvswitch/
OVS_LOG_DIR=/usr/local/var/log/openvswitch/

OVSDB_SOCK=$OVS_RUN_DIR/db.sock
OVSDB_CONF=$OVS_ETC_DIR/conf.db
OVSDB_LOG_FILE=$OVS_LOG_DIR/ovsdb-server.log
OVSDB_PID_FILE=$OVS_RUN_DIR/ovsdb-server.pid
OVS_VHOST_SUBDIR=vhost-sock

SLEEP_SECS=1
