import hashlib
import os
import json

import conf
from util.system import run,kill


enable_host_guest_fwd_port = False

def install():
    run(['sudo', '-E', 'wget', '-nc', conf.QEMU_TARBALL_URL, '-P', conf.TARBALLS_DIR])
    run(['sudo', 'tar', '-jxvf', conf.TARBALLS_DIR + conf.QEMU_TARBALL_FILE, '--directory', conf.BASE_DIR])
    run('cd ' + conf.QEMU_DIR + ' && sudo ./configure --target-list=x86_64-softmmu --enable-debug --enable-kvm --enable-numa && sudo make',
        do_shell=True)

def uninstall():
    run(['sudo', 'rm', '-rf', conf.QEMU_DIR])

class QemuVhostuser(object):
    def __init__(self, cpu_list, name, enable_kvm, snapshot, guest_mem, nsockets,
                 cores_per_socket, qcow2_image, cloud_init_iso_image, interfaces,
                 host_ssh_port, host_guest_fwd_port):
        self._cpu_list = cpu_list
        self._name = name
        self._enable_kvm = enable_kvm
        self._snapshot = snapshot
        self._guest_mem = guest_mem
        self._nsockets = nsockets
        self._cores_per_socket = cores_per_socket
        self._qcow2_image = qcow2_image
        self._cloud_init_iso_image = cloud_init_iso_image
        self._ifaces = json.loads(interfaces)
        self._host_ssh_port = host_ssh_port
        if host_guest_fwd_port is not None:
            self._host_guest_fwd_port = json.loads(host_guest_fwd_port)
        else:
            self._host_guest_fwd_port = None
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
        cmd = ['sudo']

        if self._cpu_list:
            cmd = cmd + ['taskset', '-c', self._cpu_list]
        
        cmd = cmd + [conf.QEMU_BIN,
               '-name', self._name,
               '-cpu', 'host',
               '-m', self._guest_mem,
               '-object', 'memory-backend-file,id=mem,size=' + self._guest_mem + ',mem-path=/dev/hugepages,share=on',
               '-numa', 'node,memdev=mem',
               '-mem-prealloc',
               '-smp', 'sockets=' + str(self._nsockets) + ',cores=' + str(self._cores_per_socket),
               '-device', 'e1000,netdev=netmgmt',
               ]

        netdev_string = 'user,id=netmgmt,hostfwd=tcp::' + str(self._host_ssh_port) + '-:22'
        if self._host_guest_fwd_port is not None:
            for couple_ports in self._host_guest_fwd_port:
                netdev_string = netdev_string + ',hostfwd=tcp::' + str(couple_ports["host_port"]) + '-:' + str(couple_ports["guest_port"])

        cmd = cmd + [
               '-netdev', netdev_string,
               '-drive', 'file=' + self._qcow2_image,
               '-drive', 'file=' + self._cloud_init_iso_image,
               '-nographic',
               '-pidfile', '/tmp/' + self._name + '.pid',
               ]

        if self._snapshot:
            cmd.append('-snapshot')

        if self._enable_kvm:
            cmd.append('-enable-kvm')

        prefix = self._mac_prefix()

        ind = 0
        for dev in self._ifaces:
            if 'mac' not in dev:
                dev['mac'] = prefix + format(ind, '02x')
            chardev = self._name + '_chardev' + str(ind)
            netdev = self._name + '_netdev' + str(ind)
            vectors = int(dev['queues']) * 2 + 2
            netcmd = ['-chardev',
                      'socket,id=' + chardev + ',path=' + conf.OVS_VHOST_SOCKETS_DIR + dev['port'],
                      '-netdev',
                      'type=vhost-user,id=' + netdev + ',chardev=' + chardev + ',vhostforce,queues=' + str(dev['queues']),
                      '-device',
                      'virtio-net-pci,mac=' + dev['mac'] + ',netdev=' + netdev + ',mrg_rxbuf=off,mq=on,vectors=' + str(vectors)
                  ]
            cmd = cmd + netcmd
            ind += 1

        # TODO: execute cmd
        print(cmd)
        run(cmd)
        # self._init_pid()

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
