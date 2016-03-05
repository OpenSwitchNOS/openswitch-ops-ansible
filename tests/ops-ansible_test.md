# Ansible Test Cases

- [Test connection between Ansible control machine and openswitch](#test-connection-between-Ansible-control-machine-and-openswitch)

## Test connection between Ansible control machine and openswitch
### Objective
Verify that control machine can communicate with openswitch using ssh key

### Requirements
The Virtual Mininet Test Setup is required for this test.

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
This test confirms that we can establish ssh communication between Ansible control machine and the openswitch

### Test result criteria
#### Test pass criteria
Running ping module from control machine on the openswitch succeeds.
#### Test fail criteria
Running ping module fails on the openswitch

