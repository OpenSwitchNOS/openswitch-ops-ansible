# Ansible Test Cases

- [Test to copy ssh key using ansible playbook](#test-to-copy-ssh-key-using-ansible-playbook)

## Test to copy ssh key using ansible playbook
### Objective
Verify that ssh key can be copied from control machine to openswitch and
communciation can be established.

### Requirements
The topology framework test setup is required for this test.
OSTL(physical) switch setup is used.

### Setup

#### Topology diagram

```
         +-------------+
         |             |
         |             |
         | OpenSwitch  |
         |             |
         |             |
         |             |
         +------+------+
                |sp1
                |
                |eth0
         +------+------+
         |             |
         |             |
         |  Ansible    |
         |  control    |
         |  machine    |
         +-------------+

```

### Description
This test confirms that we can establish ssh communication between Ansible
control machine and the openswitch. We use the ansible playbook to copy
the ssh key from ansible control machine to openswitch and then try
using a ping module through ansible playbook to check if we can communicate
with the openswitch.

### Test result criteria
#### Test pass criteria
Running Ansible ping module in an ansible playbook from control machine
on the openswitch succeeds.
#### Test fail criteria
Running Ansible ping module in an ansible playbook fails on the openswitch
