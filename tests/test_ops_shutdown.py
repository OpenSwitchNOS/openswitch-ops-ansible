# Copyright (C) 2016 Hewlett Packard Enterprise Development LP
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# Topology:
#
#         +-------------+
#         |             |
#         |             |
#         | OpenSwitch  |
#         |             |
#         |             |
#         |             |
#         +------+------+
#                |eth0
#                |
#                |eth0
#         +------+------+
#         |             |
#         |             |
#         |  Ansible    |
#         |  control    |
#         |  machine    |
#         +-------------+
#


from opstestfw import *
from opstestfw.switch.CLI import *
from opstestfw.switch import *


# Topology definition
topoDict = {"topoExecution": 3000,
            "topoTarget": "dut01",
            "topoDevices": "dut01 control",
            "topoLinks": "lnk01:dut01:control",
            "topoFilters": "dut01:system-category:switch,\
                            control:system-category:workstation,\
                            control:docker-image:openswitch/ansible",
            "topoLinkFilter": "lnk01:dut01:interface:eth0"}

switchMgmtIPAddr = "172.17.0.10"
ansibleCMIPAddr = "172.17.0.11"
broadcast = "172.17.0.255"
netmask = "255.255.255.0"
subnetMaskBits = 24


def opscmipconfig(dut01, control):
    global switchMgmtIPAddr
    global ansibleCMIPAddr

    info('### Configuring IP on the openswitch ###\n\n')
    retstruct = InterfaceIpConfig(deviceObj=dut01,
                                  interface="mgmt",
                                  addr=switchMgmtIPAddr,
                                  mask=subnetMaskBits,
                                  config=True)

    assert retstruct.returnCode() == 0,\
        'Configuring IP address on the switch port failed!'
    info('\n\n### Successfully configured ip on the switch! ###\n\n')

    # run ifconfig on switch bash to check the IP
    cmd = dut01.DeviceInteract(command="ifconfig")
    print cmd

    # check if the IP was configured successfully on the switch
    out = dut01.cmdVtysh(command="show run")
    info('\n\n### Running config of the switch:\n' + out + ' ###\n\n')

    info('### Configuring IP on the ansible control machine ###\n\n')
    retstruct = control.NetworkConfig(
                                ipAddr=ansibleCMIPAddr,
                                netMask=netmask,
                                broadcast=broadcast,
                                interface=control.linkPortMapping['lnk01'],
                                config=True)

    assert retstruct.returnCode() == 0,\
        'Failed to configure IP on Ansible control machine'
    info('\n\n### Successfully configured IP on control machine ###\n')

    # Confirm the IP configuration
    out = control.cmd("ifconfig " + control.linkPortMapping['lnk01'])
    info('\n\n### Ifconfig info on control machine:\n' + out + '###\n')


def checksshkeycopyplaybook(control):
    # add the ssh key identity on the control machine
    out = control.cmd("eval `ssh-agent -s`")
    print out
    out = control.cmd("ssh-add")
    print out

    ''' Run playbook to copy ssh key to authorized keys in switch
        "ANSIBLE_SCP_IF_SSH=y" is mentioned before the command
        because this variable needs to be exported-
        when the docker instance is initiated but can not be done
        through test script.'''
    info("\n\n### Copying the ssh key from control machine "
         "to switch using a playbook ###\n\n")
    out = control.cmd("ANSIBLE_SCP_IF_SSH=y ansible-playbook "
                      "/ansible/copy_public_key.yml -u root")
    print out

    # run the ping module to check that we have connectivity to the switch
    info("\n\n### checking the connectivity with the switch ###\n\n")
    out = control.cmd("ANSIBLE_SCP_IF_SSH=y ansible ops -m ping -u root")
    print out


def switchshutdown(dut01, control):
    info("\n\n### shut down the switch ###\n\n")
    out = control.cmd("ANSIBLE_SCP_IF_SSH=y ansible-playbook "
                      "/ansible/ops_shutdown.yml -u root")
    print out

    ''' when shutdown command is issued, shutdown is
        scheduled for after 60 seconds
        following sleep is to wait till the ops is shutdown.'''
    sleep(60)

    # run the ping module to check if the shutdown was successful
    info("\n\n### After the shutdown command checking "
         "if we can reach the switch ###\n\n")
    out = control.cmd("ANSIBLE_SCP_IF_SSH=y ansible ops -m ping -u root")
    print out
    assert '"ping": "pong"' in out, "Test to shutdown the openswitch failed!"
    info("Test to shutdown the openswitch was successful!")


class TestAnsibleOpsConfig:
    def setup_class(cls):
        # Test object will parse command line and formulate the env
        TestAnsibleOpsConfig.testObj = testEnviron(topoDict=topoDict)
        # Get topology object
        TestAnsibleOpsConfig.topoObj = \
            TestAnsibleOpsConfig.testObj.topoObjGet()

    def teardown_class(cls):
        TestAnsibleOpsConfig.topoObj.terminate_nodes()

    def testopsansible(self):
        dut01obj = self.topoObj.deviceObjGet(device="dut01")
        controlobj = self.topoObj.deviceObjGet(device="control")
        opscmipconfig(dut01obj, controlobj)
        checksshkeycopyplaybook(controlobj)
        switchshutdown(dut01obj, controlobj)