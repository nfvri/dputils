import conf
from util.system import run, sleep
import sys
import re


class OvsDpdk(object):
    """
    Stateless OvsDpdk objects
    """

    def __init__(self):
        self._vsctl_cmd = ['sudo', conf.OVS_DIR + '/utilities/ovs-vsctl', '--db=unix:' + conf.OVSDB_SOCK, '--no-wait']
        self._ofctl_cmd = ['sudo', conf.OVS_DIR + '/utilities/ovs-ofctl']

    def install(self):
        run(['sudo', 'mkdir', '-p', conf.BASE_DIR + '/tarballs'])
        tarball = 'openvswitch-' + conf.OVS_VERSION + '.tar.gz'
        run(['sudo', '-E', 'wget', '-nc', 'http://openvswitch.org/releases/' + tarball, '-P', conf.BASE_DIR + '/tarballs'])
        run(['sudo', 'tar', '-zxvf', conf.BASE_DIR + '/tarballs/' + tarball, '--directory', conf.BASE_DIR])
        run('cd ' + conf.OVS_DIR +
            ' && sudo ./boot.sh ' +
            ' && sudo ./configure --with-dpdk=' + conf.DPDK_BUILD +
            ' && sudo make', do_shell=True)

    def uninstall(self):
        run(['rm', '-rf', conf.OVS_DIR])

    def db_create(self):
        run(['sudo', 'rm', '-rf', conf.OVSDB_CONF])
        run(['sudo', 'mkdir', '-p', conf.OVS_ETC_DIR])
        run(['sudo', 'mkdir', '-p', conf.OVS_RUN_DIR])
        run(['sudo', conf.OVS_DIR + '/ovsdb/ovsdb-tool', 'create', conf.OVSDB_CONF, conf.OVSDB_SCHEMA])

    def db_clean(self):
        run(['sudo', 'pkill', '-KILL', 'ovsdb-server'], do_check=False)
        run('sudo rm -rf ' + conf.OVS_RUN_DIR + '/* ' +
            conf.OVS_ETC_DIR + '/* ' +
            conf.OVS_LOG_DIR + '/*',
            do_shell=True)

    def db_init(self):
        run(self._vsctl_cmd + ['init'])

    def db_start(self):
        run(['sudo', conf.OVS_DIR + '/ovsdb/ovsdb-server', '--remote=punix:' + conf.OVSDB_SOCK,
             '--remote=db:Open_vSwitch,Open_vSwitch,manager_options', '--pidfile', '--detach',
             conf.OVSDB_CONF])

    def start(self, dpdk_socket_mem=None, dpdk_lcore_mask=None, dpdk_pmd_mask=None):
        run(['sudo', 'mkdir', '-p', conf.OVS_VHOST_SOCKETS_DIR])
        # specify OVS to initialize and support DPDK ports
        run(self._vsctl_cmd + ['set', 'Open_vSwitch', '.', 'other_config:dpdk-init=true'])
        # specify huge pages directory
        run(self._vsctl_cmd + ['set', 'Open_vSwitch', '.', 'other_config:dpdk-hugepage-dir=/dev/hugepages'])
        # set path to vhost_user unix socket
        run(self._vsctl_cmd + ['set', 'Open_vSwitch', '.',
                               'other_config:vhost-sock-dir="' + conf.OVS_VHOST_SOCKETS_DIR + '"'])
        # set memory
        if dpdk_socket_mem:
            run(self._vsctl_cmd + ['set', 'Open_vSwitch', '.',
                                   'other_config:dpdk-socket-mem=' + dpdk_socket_mem])
        # set DPDK lcore threads CPU mask
        if dpdk_lcore_mask:
            run(self._vsctl_cmd + ['set', 'Open_vSwitch', '.',
                                   'other_config:dpdk-lcore-mask="0x' + dpdk_lcore_mask + '"'])
        # set PMD threads CPU mask
        if dpdk_pmd_mask:
            run(self._vsctl_cmd + ['set', 'Open_vSwitch', '.',
                                   'other_config:pmd-cpu-mask=' + dpdk_pmd_mask])
        run(
            ['sudo', conf.OVS_DIR + '/vswitchd/ovs-vswitchd', 'unix:' + conf.OVSDB_SOCK, '--pidfile', '--detach'])

    def stop(self):
        run(['sudo', 'pkill', '-KILL', 'ovs-vswitchd'], do_check=False)
        run('sudo rm -rf ' + conf.OVS_RUN_DIR + '/*', do_shell=True)

    def show(self):
        run(self._vsctl_cmd + ['show'])

    def br_add(self, br):
        run(self._vsctl_cmd + ['add-br', br, '--', 'set', 'bridge', br, 'datapath_type=netdev'])
        sleep(conf.SLEEP_SECS)

    def br_del(self, br):
        run(self._vsctl_cmd + ['del-br', br])
        sleep(conf.SLEEP_SECS)

    def br_show(self, br):
        run(self._ofctl_cmd + ['show', br])

    def dpdk_port_add(self, br, port, rx_queues=None, rx_aff=None, rx_size=None, tx_queues=None, tx_aff=None,
                      tx_size=None):
        run(self._vsctl_cmd + ['add-port', br, port, '--', 'set', 'Interface', port, 'type=dpdk'])
        sleep(conf.SLEEP_SECS)

        if rx_queues:
            run(self._vsctl_cmd + ['set', 'Interface', port, 'options:n_rxq=' + str(rx_queues)])
        if rx_size:
            run(self._vsctl_cmd + ['set', 'Interface', port, 'options:n_rxq_desc=' + str(rx_size)])
        if rx_aff:
            run(
                self._vsctl_cmd + ['set', 'Interface', port, 'other_config:pmd-rxq-affinity="' + str(rx_aff) + '"'])

        if tx_queues:
            run(self._vsctl_cmd + ['set', 'Interface', port, 'options:n_txq=' + str(tx_queues)])
        if tx_size:
            run(self._vsctl_cmd + ['set', 'Interface', port, 'options:n_txq_desc=' + str(tx_size)])
        if tx_aff:
            run(
                self._vsctl_cmd + ['set', 'Interface', port, 'other_config:pmd-txq-affinity="' + str(tx_aff) + '"'])

    def vhost_port_add(self, br, port):
        run(self._vsctl_cmd + ['add-port', br, port, '--', 'set', 'Interface', port, 'type=dpdkvhostuser'])
        sleep(conf.SLEEP_SECS)

    def port_del(self, br, port):
        run(self._vsctl_cmd + ['del-port', br, port])
        sleep(conf.SLEEP_SECS)

    def ports_dump(self, br):
        run(self._ofctl_cmd + ['dump-ports', br])

    def flow_add_port2port(self, br, in_port, out_ports):
        """
        Args:
            br: Bridge to add flows to
            in_port: Input port (e.g. 'dpdk0')
            out_ports: list of output ports (e.g. ['vhost-user1', 'vhost-user2'])

        """
        # Create a pmap to map a symbolic port name to its number, e.g. pmap['vhost-user1'] = '8'
        pmap = {}
        out = run(self._ofctl_cmd + ['show', br], get_out=True)

        # output example:  8(vhost-user1): addr:00:00:00:00:00:00
        matches = re.findall(r'(.*)\((.*)\): addr:', out)
        for m in matches:
            pmap[m[1].strip()] = m[0].strip()

        if in_port not in pmap.keys():
            sys.exit(in_port + ' is not a valid port name')
        for op in out_ports:
            if op not in pmap.keys():
                sys.exit(op + ' is not a valid port name')

        in_port_numeric = pmap[in_port]
        out_ports_numeric = ','.join([pmap[i] for i in out_ports])
        run(
            self._ofctl_cmd + ['add-flow', br, 'in_port=' + in_port_numeric + ',action=output:' + out_ports_numeric])

    def flows_del(self, br):
        run(self._ofctl_cmd + ['del-flows', br])
        sleep(conf.SLEEP_SECS)

    def flows_dump(self, br):
        run(self._ofctl_cmd + ['dump-flows', br])
