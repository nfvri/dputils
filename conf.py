# vim: set syntax=python
BASE_DIR = '/opt/nfvacc'

DPDK_VERSION = '16.07.2'
DPDK_VERSION = '16.11.2'

DPDK_XZ_FILE = 'dpdk-' + DPDK_VERSION + '.tar.xz'
DPDK_XZ_URL = 'http://fast.dpdk.org/rel/' + DPDK_XZ_FILE
DPDK_XZ_DIR = BASE_DIR + '/tarballs/'
DPDK_DIR = BASE_DIR + '/dpdk-stable-' + DPDK_VERSION

NR_HUGEPAGES = 16384

DPDK_TARGET = 'x86_64-native-linuxapp-gcc'
DPDK_BUILD = DPDK_DIR + '/' + DPDK_TARGET
OVS_VERSION = '2.6.0'
OVS_DIR = BASE_DIR + '/openvswitch-' + OVS_VERSION
OVSDB_SCHEMA = OVS_DIR + '/vswitchd/vswitch.ovsschema'

#OVSDB_RUN_DIR=$BASE_DIR/openvswitch-${OVS_VERSION}-runtime
OVSDB_RUN_DIR = '/usr/local/'

OVS_RUN_DIR = '/usr/local/var/run/openvswitch/'
OVS_ETC_DIR = '/usr/local/etc/openvswitch/'
OVS_LOG_DIR = '/usr/local/var/log/openvswitch/'

OVSDB_SOCK = OVS_RUN_DIR + '/db.sock'
OVSDB_CONF = OVS_ETC_DIR + '/conf.db'
OVSDB_LOG_FILE = OVS_LOG_DIR + '/ovsdb-server.log'
OVSDB_PID_FILE = OVS_RUN_DIR + '/ovsdb-server.pid'
OVS_VHOST_SOCKETS_DIR = OVS_RUN_DIR + 'vhost-sock/'

SLEEP_SECS = '1'

QEMU_VERSION = '2.7.0'
QEMU_PKG_FILE = 'qemu-' + QEMU_VERSION + '.tar.bz2'
QEMU_PKG_URL = 'http://wiki.qemu-project.org/download/' + QEMU_PKG_FILE
QEMU_PKG_DIR = BASE_DIR + '/tarballs/'
QEMU_DIR = BASE_DIR + '/qemu-' + QEMU_VERSION + '/'
QEMU_BIN = QEMU_DIR + '/x86_64-softmmu/qemu-system-x86_64'

