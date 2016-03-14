# Ansible Test Cases

- [Test the ops shutdown operation using ansible playbook](#test-the-ops-shutdown-operation-using-playbook)

## Test the openswitch shutdown operation using playbook
### Objective
Verify that openswitch can be shutdown using the ansible playbook

### Requirements
The Virtual Mininet Test Setup is required for this test.

### Setup

#### Topology diagram

```
    +------------------+                           +--------------------+
    |     Ansible      |                           |                    |
    | control machine  |eth0                   eth0|     OpenSwitch     |
    |                  +--------------------------+|                    |
    |                  |                           |                    |
    |                  |                           |                    |
    +------------------+                           +--------------------+
```

### Description
This test confirms that we can shutdown the openswitch using ansible playbook through control machine

### Test result criteria
#### Test pass criteria
Openswitch is shutdown and ping fails
#### Test fail criteria
Openswitch is still running and ping is successful

