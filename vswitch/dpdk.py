import conf
from util.system import run

class Dpdk(object):
    def install(self):
        run(['sudo','mkdir', '-p', conf.TARBALLS_DIR])
        run(['sudo', '-E', 'wget', '-nc', conf.DPDK_TARBALL_URL, '-P', conf.TARBALLS_DIR])
        run(['sudo', 'tar', 'xf', conf.TARBALLS_DIR + conf.DPDK_TARBALL_FILE, '-C', conf.BASE_DIR])
        run('cd ' + conf.DPDK_DIR + ' && sudo make install T=' + conf.DPDK_TARGET + ' DESTDIR=install', do_shell=True)

    def uninstall(self):
        run(['sudo', 'rm', '-rf', conf.DPDK_DIR])

    def unload_modules(self):
        run(['sudo', 'rmmod', '-f', 'igb_uio'])

    def load_modules(self):
        run(['sudo', 'modprobe', 'uio'])
        run(['sudo', 'insmod', conf.DPDK_DIR + '/x86_64-native-linuxapp-gcc/kmod/igb_uio.ko'])

    def mount_huge(self):
        run(['sudo', 'sysctl', '-w', 'vm.nr_hugepages=' + str(conf.NR_HUGEPAGES)])
        run(['sudo', 'mount', '-t', 'hugetlbfs', 'none', '/dev/hugepages'])

    def unmount_huge(self):
        run(['sudo', 'umount', '/dev/hugepages'])

    def bind_status(self):
        if conf.DPDK_VERSION == '17.11.3' or conf.DPDK_VERSION == '18.11.1':
            tools_dir = '/usertools/'
        else:
            tools_dir = '/tools/'

        run(['sudo', conf.DPDK_DIR + tools_dir + 'dpdk-devbind.py', '--status'])

    def bind_igb_uio(self, ifaces):
        """
        Bind interfaces to the igb_uio driver

        Args:
            ifaces: list of interfaces to bind, e.g. ['0000:01:00.0', '0000:01:00.1']
        """
        if conf.DPDK_VERSION == '17.11.3' or conf.DPDK_VERSION == '18.11.1':
            tools_dir = '/usertools/'
        else:
            tools_dir = '/tools/'

        run(['sudo', conf.DPDK_DIR + tools_dir + 'dpdk-devbind.py', '--bind=igb_uio'] + ifaces)

    def unbind_to(self, ifaces, drv):
        """
        Unbind interfaces from the igb_uio driver back to ixgbe, e1000, etc.

        Args:
            ifaces: list of interfaces to unbind, e.g. ['0000:01:00.0', '0000:01:00.1']
            drv: driver to bind interfaces back to, e.g. ixgbe, e1000, etc.
        """
        if conf.DPDK_VERSION == '17.11.3' or conf.DPDK_VERSION == '18.11.1':
            tools_dir = '/usertools/'
        else:
            tools_dir = '/tools/'

        run(['sudo', conf.DPDK_DIR + tools_dir + 'dpdk-devbind.py', '--unbind'] + ifaces)
        run(['sudo', conf.DPDK_DIR + tools_dir + 'dpdk-devbind.py', '--bind=' + drv] + ifaces)
