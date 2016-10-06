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
OVSDB_DB_SOCK=$OVSDB_RUN_DIR/var/run/openvswitch/db.sock
OVSDB_CONF=$OVSDB_RUN_DIR/etc/openvswitch/conf.db
OVSDB_LOG_FILE=$OVSDB_RUN_DIR/var/log/openvswitch/ovsdb-server.log
OVSDB_PID_FILE=$OVSDB_RUN_DIR/var/run/openvswitch/ovsdb-server.pid
OVS_RUN_DIR=/var/run/openvswitch/
SLEEP_SECS=1
