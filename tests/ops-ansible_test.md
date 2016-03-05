# Ansible Test Cases

- [Test to copy ssh key using ansible playbook](#test-to-copy-ssh-key-using-ansible-playbook)

## Test to copy ssh key using ansible playbook
### Objective
Verify that ssh key can be copied from conftol machine to openswitch and communciation can be established.

### Requirements
The topology framework test setup is required for this test.

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
                |eth0
                |
                |eth1
         +------+------+
         |             |
         |             |
         |  Ansible    |
         |  control    |
         |  machine    |
         +-------------+

```

### Description
This test confirms that we can establish ssh communication between Ansible control machine and the openswitch

### Test result criteria
#### Test pass criteria
Running ping module from control machine on the openswitch succeeds.
#### Test fail criteria
Running ping module fails on the openswitch
