# Ops-Ansible test design document

## High level diagram

```
    +------------------+                           +--------------------+
    |     Ansible      |                           |                    |
    | control machine  |                           |     OpenSwitch     |
    |        +         |eth0+-----------------+eth0|                    |
    |Ansible OpenSwitch|                           |(Container/Physical)|
    |  Roles (switch)  |                           |                    |
    +------------------+                           +--------------------+
```

## How to setup Ansible control machine

We will create a Ansible control machine with the latest Ansible core
and modules core for the final testing, here is the steps to go through
to make it manually:

1. Clone the latest Ansible 2.x code

   Retrieve the Ansible 2.x code from the github:

   ```
   $ git clone git@github.com:ansible/ansible.git --recursive
   ```

2. Check the Ansible OpenSwitch library

   Make sure that you have the latest Ansible OpenSwitch library:

   ```
   $ cd ansible
   $ find . -name 'openswitch.*' -print
   ./lib/ansible/module_utils/openswitch.py
   ./lib/ansible/utils/module_docs_fragments/openswitch.py
   ```

3. Check the Ansible OpenSwitch module

   Make sure that you have `ops_template.py` located under `network`
   directory:

   ```
   $ find . -name "ops_*" -print
   ./network/openswitch/ops_template.py
   ```

4. Install Ansible to your environment

   You can install the ansible core and modules with OpenSwitch support
   by typing `make install` at the top directory:

   ```
   $ cd ../../../..
   $ sudo make install
   ```

   Please use your favorite way to install your python module, if you
   don't want to install in the system wide location, as ansible is
   nothing but the python modules.