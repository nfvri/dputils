import conf
from util.system import run


class Dpdk(object):
    def install(self):
        run(['sudo','mkdir', '-p', conf.BASE_DIR + '/tarballs'])
        run(['sudo', '-E', 'wget', '-nc', conf.DPDK_XZ_URL, '-P', conf.DPDK_XZ_PATH])
        run(['sudo', 'tar', 'xf', conf.DPDK_XZ_PATH + conf.DPDK_XZ_FILE, '-C', conf.BASE_DIR])
        run('cd ' + conf.DPDK_DIR + ' && sudo make install T=' + conf.DPDK_TARGET + ' DESTDIR=install', do_shell=True)

    def uninstall(self):
        run(['sudo', 'rm', '-rf', conf.DPDK_DIR])

    def unload_modules(self):
        run(['sudo', 'rmmod', 'igb_uio'])

    def load_modules(self):
        run(['sudo', 'modprobe', 'uio'])
        run(['sudo', 'insmod', conf.DPDK_DIR + '/x86_64-native-linuxapp-gcc/kmod/igb_uio.ko'])

    def mount_huge(self):
        run(['sudo', 'mount', '-t', 'hugetlbfs', 'none', '/dev/hugepages'])

    def unmount_huge(self):
        run(['sudo', 'umount', '/dev/hugepages'])

    def bind_status(self):
        run(['sudo', conf.DPDK_DIR + '/tools/dpdk-devbind.py', '--status'])

    def bind_igb_uio(self, ifaces):
        """
        Bind interfaces to the igb_uio driver

        Args:
            ifaces: list of interfaces to bind, e.g. ['0000:01:00.0', '0000:01:00.1']
        """
        run(['sudo', conf.DPDK_DIR + '/tools/dpdk-devbind.py', '--bind=igb_uio'] + ifaces)

    def unbind_to(self, ifaces, drv):
        """
        Unbind interfaces from the igb_uio driver back to ixgbe, e1000, etc.

        Args:
            ifaces: list of interfaces to unbind, e.g. ['0000:01:00.0', '0000:01:00.1']
            drv: driver to bind interfaces back to, e.g. ixgbe, e1000, etc.
        """
        run(['sudo', conf.DPDK_DIR + '/tools/dpdk-devbind.py', '--unbind'] + ifaces)
        run(['sudo', conf.DPDK_DIR + '/tools/dpdk-devbind.py', '--bind=' + drv] + ifaces)
