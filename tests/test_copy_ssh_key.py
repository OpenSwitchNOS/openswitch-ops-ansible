# Copyright (C) 2016 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.


TOPOLOGY = """
#         +-------------+
#         |             |
#         |             |
#         | OpenSwitch 1|
#         |             |
#         |             |
#         |             |
#         +------+------+
#                |eth0
#                |
#                |eth1
#         +------+------+
#         |             |
#         |             |
#         |  Host 1     |
#         | (control    |
#         |  machine)   |
#         +-------------+
#
# Nodes
[type=openswitch name="OpenSwitch 1"] ops1
[type=host name="Host 1" image="openswitch/ansible:latest"] hs1
#
# Links
[force_name=eth0] ops1:eth0
ops1:eth0 -- hs1:eth1
"""


HS1_IP_MASK = '10.10.10.1/24'
OPS1_IP_MASK = '10.10.10.2/24'
HS1_IP = '10.10.10.1'
OPS1_IP = '10.10.10.2'
PINGCNT = 2
PINGINT = 0.1


def test_copy_ssh_key(topology, step):
    ops1 = topology.get('ops1')
    hs1 = topology.get('hs1')

    assert ops1 is not None
    assert hs1 is not None

    # configure IP on host
    hs1.libs.ip.interface('eth1', addr=HS1_IP_MASK, up=True)

    # configure IP on switch for interface 1
    with ops1.libs.vtysh.ConfigInterface('eth0') as ctx:
        ctx.ip_address(OPS1_IP_MASK)
        ctx.no_shutdown()

    # Check the ops connectivity with host
    ping = hs1.libs.ping.ping(PINGCNT, OPS1_IP, PINGINT)
    assert ping['transmitted'] == ping['received'] == 2

    ops1("ifconfig", shell='bash')

    # Create ansible config file with inventory
    hs1("echo \"[defaults]\n"
        "inventory=/etc/ansible/hosts\" > /etc/ansible/ansible.cfg")

    # Add Ip of the switch to the host file on the control machine
    hs1("echo \"[ops] \n10.10.10.2 ansible_ssh_port=22\" > /etc/ansible/hosts")

    # Debug
    hs1("cat /etc/ansible/hosts")
    hs1("cat /etc/ansible/ansible.cfg")

    # generate ssh key
    out = hs1("ssh-keygen -t rsa -f id_rsa -N ''")

    # start the ssh agent
    hs1("eval `ssh-agent -s`")

    # Add the identity
    hs1("ssh-add id_rsa")

    # run playbook to copy ssh key to authorized keys in switch
    out = hs1("ANSIBLE_SCP_IF_SSH=y ansible-playbook"
              " /ansible/copy_public_key.yml -u root")
    step(out)

    # run ansible ping module to check the connectivity with the switch
    out = hs1("ANSIBLE_SCP_IF_SSH=y ansible ops -m ping")
