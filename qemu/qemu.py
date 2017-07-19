import hashlib
import os

import conf
from util.system import run,kill


def install():
    run(['sudo', '-E', 'wget', '-nc', conf.QEMU_PKG_URL, '-P', conf.QEMU_PKG_DIR])
    run(['sudo', 'tar', '-jxvf', conf.QEMU_PKG_DIR + conf.QEMU_PKG_FILE, '--directory', conf.BASE_DIR])
    run('cd ' + conf.QEMU_DIR + ' && sudo ./configure --target-list=x86_64-softmmu --enable-debug --enable-kvm --enable-numa && sudo make',
        do_shell=True)

def uninstall():
    run(['sudo', 'rm', '-rf', conf.QEMU_DIR])

class QemuVhostuser(object):
    def __init__(self, cpu_list, name, enable_kvm, guest_mem, nsockets,
                 cores_per_socket, qcow2_image, vhostuser_ports_names,
                 vhostuser_ports_nqueues):
        self._cpu_list = cpu_list
        self._name = name
        self._enable_kvm = enable_kvm
        self._guest_mem = guest_mem
        self._nsockets = nsockets
        self._cores_per_socket = cores_per_socket
        self._qcow2_image = qcow2_image
        self._vhostuser_ports_names = vhostuser_ports_names
        self._vhostuser_ports_nqueues = vhostuser_ports_nqueues
        self._vhostuser_ports_macs = []
        self._pid = -1
        self._pidfile = None

    def _mac_prefix(self):
        """
        Compute a unique prefix for the first 3 bytes of all MAC addresses, 
        based on the guest name
        """
        sig = hashlib.md5(self._name.encode('utf-8')).hexdigest()
        return sig[0:2] + ':' + sig[2:4] + ':' + sig[4:6] + ':00:00:'

    def _init_pid(self):
        with open(self._pidfile, 'r') as f:
            self._pid = f.read().replace('\n', '')

    def start(self):
        cmd = ['taskset', '-c', self._cpu_list, conf.QEMU_BIN,
               '-name', self._name,
               '-cpu', 'host',
               '-m', self._guest_mem,
               '-object', 'memory-backend-file,id=mem,size=' + self._guest_mem + ',mem-path=/dev/hugepages,share=on',
               '-numa', 'node,memdev=mem',
               '-mem-prealloc',
               '-smp', 'sockets=' + str(self._nsockets) + ',cores=' + str(self._cores_per_socket),
               '-drive', 'file=' + self._qcow2_image,
               '-nographic',
               '-snapshot',
               '-pidfile', '/tmp/' + self._name + '.pid',
               ]

        if self._enable_kvm:
            cmd.append('-enable-kvm')

        prefix = self._mac_prefix()

# TODO: user-specified MACs

        ind = 0
        for (port_name, nqueues) in zip(self._vhostuser_ports_names.split(','),
                                   self._vhostuser_ports_nqueues.split(',')):
            chardev_id = self._name + '_chardev' + str(ind)
            netdev_id = self._name + '_netdev' + str(ind)
            vectors = int(nqueues) * 2 + 2
            mac = prefix + format(ind, '02x')
            self._vhostuser_ports_macs.append(mac)
            netcmd = ['-chardev', 'socket,id=' + chardev_id + ',path=' + conf.VHOST_SOCK_DIR + port_name,
                      '-netdev', 'type=vhost-user,id=' + netdev_id + ',chardev=' + chardev_id + ',vhostforce,queues=' + nqueues,
                      '-device', 'virtio-net-pci,mac=' + mac + ',netdev=' + netdev_id + ',mq=on,vectors=' + str(vectors)
                      ]
            cmd = cmd + netcmd
            ind += 1

        # TODO: execute cmd
        print(cmd)
        self._init_pid()

    """
     sudo -E  taskset -c 0x20 qemu-system-x86_64 
       -name $VM_NAME 
       -cpu host 
       -enable-kvm 
       -m $GUEST_MEM  // e.g. 3072M
       -object memory-backend-file,id=mem,size=$GUEST_MEM,mem-path=/dev/hugepages,share=on
       -numa node,memdev=mem 
       -mem-prealloc 
       -smp sockets=1,cores=2 
       -drive file=$QCOW2_IMAGE 
    
    -chardev socket,id=char2,path=/usr/local/var/run/openvswitch/vhost-user-2
    -netdev type=vhost-user,id=mynet2,chardev=char2,vhostforce,queues=$q
    -device virtio-net-pci,mac=00:00:00:00:00:02,netdev=mynet2,mq=on,vectors=$v

    $v = $q*2 + 2

       -chardev socket,id=char0,path=$VHOST_SOCK_DIR/dpdkvhostuser0 
       -netdev type=vhost-user,id=mynet1,chardev=char0,vhostforce 
       -device virtio-net-pci,mac=00:00:00:00:00:01,netdev=mynet1,mrg_rxbuf=off

       -chardev socket,id=char1,path=$VHOST_SOCK_DIR/dpdkvhostuser1 
       -netdev type=vhost-user,id=mynet2,chardev=char1,vhostforce 
       -device virtio-net-pci,mac=00:00:00:00:00:02,netdev=mynet2,mrg_rxbuf=off
      
      --nographic 
       -snapshot

    """

    def stop(self):
        kill(self._pid)
        os.remove(self._pidfile)
