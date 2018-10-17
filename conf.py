# vim: set syntax=python
BASE_DIR = '/opt/nfvacc'

# OVS-DPDK switch compatibility table
# (http://docs.openvswitch.org/en/latest/faq/releases/)
# OVS   DPDK
# 2.6.x	16.07.2
# 2.7.x	16.11.2
# 2.10.x	17.11.3

DPDK_VERSION = '16.07.2'
DPDK_VERSION = '16.11.2'
DPDK_VERSION = '17.11.3'
OVS_VERSION = '2.6.0'
OVS_VERSION = '2.7.0'
OVS_VERSION = '2.10.0'
QEMU_VERSION = '2.7.0'
QEMU_VERSION = '2.12.0'

TARBALLS_DIR = BASE_DIR + '/tarballs/'

DPDK_TARBALL_FILE = 'dpdk-' + DPDK_VERSION + '.tar.xz'
DPDK_TARBALL_URL = 'http://fast.dpdk.org/rel/' + DPDK_TARBALL_FILE
DPDK_DIR = BASE_DIR + '/dpdk-stable-' + DPDK_VERSION
NR_HUGEPAGES = 16384
DPDK_TARGET = 'x86_64-native-linuxapp-gcc'
DPDK_BUILD = DPDK_DIR + '/' + DPDK_TARGET

OVS_TARBALL_FILE = 'openvswitch-' + OVS_VERSION + '.tar.gz'
OVS_TARBALL_URL = 'http://openvswitch.org/releases/' + OVS_TARBALL_FILE
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
OVS_VHOST_SOCKETS_DIR = OVS_RUN_DIR

SLEEP_SECS = '1'

QEMU_TARBALL_FILE = 'qemu-' + QEMU_VERSION + '.tar.bz2'
QEMU_TARBALL_URL = 'http://wiki.qemu-project.org/download/' + QEMU_TARBALL_FILE
QEMU_DIR = BASE_DIR + '/qemu-' + QEMU_VERSION + '/'
QEMU_BIN = QEMU_DIR + '/x86_64-softmmu/qemu-system-x86_64'

