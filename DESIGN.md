# OpenSwitch Ansible Roles and sample playbooks

## Overview

Here is the quote from official Ansible site:

> Ansible is a radically simple IT automation platform that makes your
> applications and systmes easier to deploy.  Avoid writing scripts or
> custom code to deploy and update your applications - automate in a
> language that approaches plain English, using SSH, with no agents to
> install on remote systems.

OpenSwitch follows this philosophy and brings this simplicity into the
networking industry by providing the simple yet powerful APIs for Ansible
to interact with.

As Ansible doesn't require any agents on the remote systems as mentioned
above, and OpenSwitch is the remote system in this context, OpenSwitch
doesn't need the repository to host the software which runs on the switch.
Instead, [ops-ansible](http://git.openswitch.net/cgit/openswitch/ops-ansible)
repository hosts usuful tools which will run on the control machine,
along with the Ansible core and the modules.


## Modules

OpenSwitch Ansible support is achieved through those four modules:

1. OpenSwitch APIs
2. Ansible OpenSwitch module
3. Ansible playbooks and inventroy files

Additionally, operator can use the Ansible OpenSwitch Roles provided
by the OpenSwitch community:

4. Optional Ansible OpenSwitch Roles

Among those fhour, only OpenSwitch APIs will be on the actual switch
and the rest will be on the control machine.


## Design

Here is the high level design diagram to explain:

1. Interaction between the Ansible control machine and OpenSwitch
2. Indivisual building blocks both in control machine and OpenSwitch

```
         +-----------------------------------------------+
         |            Control machine (e.g. laptop)      |
         |                                               |
         |       Option A                 Option B       |
         |  +-----------------+      +-----------------+ |
         |  |    Playbooks    |      |    Playbooks    | |
         |  +-----------------+      +-----------------+ |
         |  +-----------------+      +-----------------+ |
         |  | Inventory files |      | Inventory files | |
         |  +-----------------+      +-----------------+ |
         |  +-----------------+      +-----------------+ |
         |  | Ansible Jinja2  |      |     Ansible     | |
         |  | template files  |      | OpenSwitch Roles| |
         |  |    (Optional)   |      |(router, bgp etc)| |
         |  +-----------------+      +-----------------+ |
         |           |                        |          |
         |           v                        v          |
         |  +------------------------------------------+ |
         |  |           Ansible 2.1 and above          | |
         |  | +---------------+     +----------------+ | |
         |  | |ops_template.py|     |  ops_facts.py  | | |
         |  | |  for config   |     |   for facts    | | |
         |  | +---------------+     +----------------+ | |
         |  +------------------------------------------+ |
         +-----------------------------------------------+
                                 ^
                                 | Ansible transport (e.g. ssh)
                                 v
         +-----------------------------------------------+
         |                  OpenSwitch                   |
         |    +---------------+     +---------------+    |
         |    |  Declarative  |     |  RESTful API  |    |
         |    | Config(DC) API|     |      for      |    |
         |    |   for config  |     |     facts     |    |
         |    +-------------- +     +---------------+    |
         |    +-------------------------------------+    |
         |    |                                     |    |
         |    |            OVSDB database           |    |
         |    |                                     |    |
         |    +-------------------------------------+    |
         |    +---------+ +--------+ +-------+           |
         |    | switchd | |  bgpd  | | ospfd |  ...      |
         |    +---------+ +--------+ +-------+           |
         +-----------------------------------------------+
```


## References

- [www.ansible.com](http://www.ansible.com)
- [Ansible Galaxy](https://galaxy.ansible.com/)
- [Ansible core](https://github.com/ansible/ansible)
- [Ansible modules core](https://github.com/ansible/ansible-modules-core)
