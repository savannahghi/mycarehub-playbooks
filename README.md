FyJ Playbooks
=============

This repo is a central location for all ansible playbooks used within the Fahari ya Jamii program.

Why?

- minimizes copy pasting of playbooks between project repos e.g. KenyaEMR project repo having MySQL playbooks that the IL project repo also has.
- single reference for writing/running playbooks.
- enforce best practices through design/review.

`main` is considered the main branch and it should be considered that at all times, production servers' reality corresponds to the `main` branch.
If this is not the case, it should be quickly rectified by updating `main` via a pull request that deploys the new reality.

To understand the rationale behind this repo and know how to use it effectively, you are required to understand what Ansible is,
how it works and specifically the following Ansible components:

- [Roles](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html)
- [Playbooks](https://docs.ansible.com/ansible/latest/user_guide/playbooks.html)
- [Inventories](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html)

Reporsitory Structure:
----------------------

- **inventories**: host configurations for different environments.
- **libs**: collection of roles used to defined reusable behaviour.
- **plays\\*\*\\\*.yml**: the different playbooks.
- **ansible.cfg**: configuration that should be used when running ansible.
- **ssh.cfg**: collection of ssh connection configurations to hosts that needs to be maintained e.g. prod hosts. This file **MUST NEVER** be included as part of the repository.
- **requirements.txt**: python packages that need to be installed to use this repo.
- **README.md**: me!
