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

Prerequisites
-------------
Before running the playbooks, you will need to ensure you have `Ansible 2.14` or above installed on the [control node](https://docs.ansible.com/ansible/latest/getting_started/index.html#getting-started-with-ansible). Check the Ansible [installation docs](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#installing-ansible) on how to do that.

After a successful Ansible installation, you will also need to install the [community.general](https://galaxy.ansible.com/community/general) Ansible Collection using the following command:
```bash
ansible-galaxy collection install community.general
```

Optionally, if you would also want to have playbook output stored locally on files for future reference, you need to create the logs directory at `/var/log/ansible/hosts`. Ensure the directory is writable by the user running Ansible, or to simply things, make the directory writable by any user. This can be achieved using the following commands:
```bash
# Create the logs directory
sudo mkdir -p /var/log/ansible/hosts
# Make the directory writable to any user
sudo chmod a=rwx /var/log/ansible/hosts
```

### Working with Teleport Hosts
Some of the hosts defined in the inventory are only accessible through a [Teleport server](https://goteleport.com/docs/). As such, special configuration on the Ansible control node is required. This can be achieved using the following steps:
> Note: Unless specified otherwise, the instructions and examples from this section henceforth will use a Teleport server hosted at `https://test.teleport.fahariyajamii.org`, a Teleport user named `barakobama` and a local user account *(on the control node)* named `barak`.
- First, ensure you have Teleport installed on the control node. Check the Teleport [installation docs](https://goteleport.com/docs/installation/) on how to do that.
- Ensure you have ample access on the target hosts through Teleport. Use the following commands to check this:
  1. Login on Teleport from the terminal using the following command:
    ```bash
    tsh login --proxy=test.teleport.fahariyajamii.org --user=barakobama
    ```
  2. List the Teleport nodes/hosts accessible to you using the following command:
    ```bash
    tsh ls
    ```
    Ensure the hosts you aim to target are listed.

    Note that this only tells you whether you have access to the target host but not whether you have sufficient privileges on the target host to run the desired playbooks. For this, check the playbook README and consult the Teleport admin.
- Use the following command to generate a ssh config for Teleport:
  ```bash
  # NOTE: Before running this, ensure that the "~/.ssh/teleport" folder exists or create one if none exists.
  tsh config | sed 's/^Host/Match Host/' | sed '/Match Host/s/ /,/3' > ~/.ssh/teleport/ssh_config
  ```

  Assuming that the Teleport server in use is hosted at `https://test.teleport.fahariyajamii.org`, the Teleport user is named `barakobama` and the local user account is named `barak`, the generated file `~/.ssh/teleport/ssh_config`, should look similar to this:
  ```cfg  
  #
  # Begin generated Teleport configuration for test.teleport.fahariyajamii.org:443 from `tsh config`
  #
  
  # Common flags for all test.teleport.fahariyajamii.org hosts
  Match Host *.test.teleport.fahariyajamii.org,test.teleport.fahariyajamii.org
      UserKnownHostsFile "/home/barak/.tsh/known_hosts"
      IdentityFile "/home/barak/.tsh/keys/test.teleport.fahariyajamii.org/barakobama"
      CertificateFile "/home/barak/.tsh/keys/test.teleport.fahariyajamii.org/barakobama-ssh/test.teleport.fahariyajamii.org-cert.pub"
      PubkeyAcceptedKeyTypes +ssh-rsa-cert-v01@openssh.com
      HostKeyAlgorithms ssh-rsa-cert-v01@openssh.com
  
  # Flags for all test.teleport.fahariyajamii.org hosts except the proxy
  Match Host *.test.teleport.fahariyajamii.org,!test.teleport.fahariyajamii.org
      Port 3022
      ProxyCommand "/usr/local/bin/tsh" proxy ssh --cluster=test.teleport.fahariyajamii.org --proxy=test.teleport.fahariyajamii.org %r@%h:%p
  
  # End generated Teleport configuration
  ```

  The important thing to note is that each host specification  starts with the `Match` keyword and that each host declaration in the `Match` clause is separated by a comma without any spaces in between.

  That's it, you should be good to go :thumbsup:.


Running
-------

First, `pip install -r requirements.txt`.

*Some inventories may require ansible vault keys/passwords so consult the playbook owners for the same*

Once you have the roles written, the playbook specified and the inventory laid out, you can run the playbooks as follows:

`ansible-playbook -i inventories/<inventory> plays/<playbook>`

Using a playbook named `app.yml` *(see below for an example of such a playbook)*:

`ansible-playbook -i inventories/inventory app.yml`

You can limit the run to a specific role by using tags e.g.:

`ansible-playbook -i inventories/inventory --tags pg_db app.yml`

You can also limit the run to a specific host but this runs the roles that the host has been grouped to.

`ansible-playbook -i inventories/inventory --limit host1 app.yml`

Ansible only cares about groups when it comes to grouping hosts or assigning variables to those groups.
When running playbooks, the groups are just used to get the hosts. So for example, you'd think that running:

`ansible-playbook -i inventories/inventory --limit postgresql_servers app.yml`

will run the `postgresql` role alone. Instead it will run both `pg_db` and `postgresql` because the group `postgresql_servers` contains `host1`.

Contributing
------------

### Reporsitory Structure:

- **inventories**: host configurations for different environments.
- **libs**: collection of roles used to defined reusable behaviour.
- **plays\\*\*\\\*.yml**: the different playbooks.
- **ansible.cfg**: configuration that should be used when running ansible.
- **ssh.cfg**: collection of ssh connection configurations to hosts that needs to be maintained e.g. prod hosts. This file **MUST NEVER** be included as part of the repository.
- **requirements.txt**: python packages that need to be installed to use this repo.
- **README.md**: me!

### Rules for this repo

- Changes to this repo are made via Pull Request
- Before anything is merged to `main` it has to be deployed first.
  In other words, the pre-merge step involves the deployment of any playbooks changed by the Merge Request.
  This ensures that `main` always reflect the same reality as what's in servers.
- All modules and plugins should be specified using their fully-qualified collection name (FQCN). See [here](https://docs.ansible.com/ansible/latest/porting_guides/porting_guide_2.10.html#ansible-2-10-porting-guide) for details.

*Exceptions to these rules can be granted during PR review with good reason*

### Roles

TLDR: Treat roles like parameterized pure functions. Composition > Inheritance.

- Add roles to the `libs` directory
- All variables used by the role need to be specified in `libs/<role_name>/defaults/main.yml` with either sensible defaults or blanks that can be validated.
  To avoid accidents after running roles without specifying their variables, set variables to their most safest default.
  For instance, if a role configures an application that sends costly SMSs, the variable that enables this should default to `false`.
  If a variable cannot have a sensible default, it should be left blank and validated that it has been specified by checking that it is not blank.
  Usually this can be done by the first task in the role. For example:

  ```yaml
  # first task in a role
  - name: Check if required vars have been defined
    ansible.builtin.fail: msg="{{ item.name }} is not defined"
    loop:
        - {"name": "variable1", "value": "{{ variable1 }}"}
        - {"name": "variable2", "value": "{{ variable2 }}"}
    when: not item.value
    tags: ["my_role"]
  ```

- Each task specified in the role needs to be tagged with the role name i.e. `tags: ["role_name"]`. This is used when running playbooks to limit which role runs (or not).
- Each task should have a sensible `name` entry. This makes it easy to understand what task is running and also acts as documentation.
- The role should do only one thing and do it well. A good way of figuring it out if this is achieved is considering if another role is doing something similar or partly similar.
  This would indicate that a new role needs to be made to do these common tasks. For example, creating databases in Postgres is a common enough task to be a role on its own (it is -> `pg_db`).
  Use a programming language function as a basis for how to think about this.
- Based on the previous point, the role needs to be parameterized. This means that it takes variables that allow it to be reused by different playbooks. For example the `pg_db` role takes the
  database name to be created and the database user so as to make it the owner of that database. This allows it to be used to create many different databases for different projects.
- Prefix all variables with the name of the role or something equivalent. Ansible treats variables as globals instead of namespacing them to roles/playbooks.
  This means that different role variables can clash with each other so always prefix your role variable names.
- Related to the previous point, avoid as much as possible the usage of variables (and templates!) in the role's tasks that are outside those defined in `libs/<role_name>/defaults/main.yml` or `libs/<role_name>/templates/` respectively. This ensures that a role only uses the variables and templates that defined inside its directory making debugging easier.
- If the role deploys an application that runs processes and/or owns directories/files, the role should make a **system user** for that application. DO NOT use the deploying user as the application user.
  This is partly for security reasons but mostly to reduce using variables outside the role e.g. the deploying user.
- Try if you can to make an *anti-role* to your role. This *anti-role* should undo what your role does (based on the same variables) to enable playbooks to be run to setup as well to destroy.
- Roles should setup all their dependencies **UNLESS** those dependencies can be reused by other roles.
  For example, an application role can install system libraries, system users, directories that it needs because those are specific to it while it can opt not to create databases because that's a common task.
  This also means that a role can/should assume that it's part of a hierarchy and that its dependencies may have already been setup. For example, the *pg_db* role assumes that postgres exists on the host it's being run on.
  It's useful for roles like this to check if their dependency exists and fail otherwise.

### Inventories

An inventory in this design primarily serves 3 purposes:

- Define hosts and how ansible can connect to them
- Assign those hosts to the appropriate groups that playbooks will target.
- Set the variables (if applicable) for each group and host. This makes it the primary source for playbook/role variables.

An inventory generally reflects an application/system environment.
For example, there could be a **prod** inventory that specified hosts, groups and variables for production deploys.
This ensures that the hosts, groups and variables are isolated from any other environment (inventory).
For instance, this allows an environment to enable celery with `enable_celery: true` variable while another environment uses `enable_celery: false`.

- Inventories are added in the `inventories` directory
- Each inventory should have a `host_vars`, `group_vars` and `hosts` directories.
- Add host aliases to `inventories/hosts/hosts` ini file e.g.:

  ```ini
  host1 ansible_host=....
  host2 ansible_host=....
  ```

  Host aliases are very powerful as you can specify different aliases for the same server making it behave like it's multiple servers.
  Essentially, a Host alias is just a pointer to an ssh connection string. By using an external ssh config, you can trick ansible to treat the
  same ssh connection string as multiple servers meaning you can run playbooks in those "independent" multiple servers. This is crucial to running playbooks for
  multi-server apps where the app is in one server, it's database in another, it's message queue in another and so forth.
  However, you can't alias an ansible host alias to another ansible host alias, only to an external ssh config host i.e.:

  ```ini
  # this DOES NOT work
  host1 ansible_host=...
  host2 ansible_host=host1
  ```

- Add host ini files to `inventory/hosts` that correspond to playbook filenames which assign hosts to the groups that the playbook is defined. Using the example playbook below (named `app.yml`), add a `app` file to `inventory/hosts` that looks like:

  ```ini
  [postgresql_servers]
  host1

  [app_db_servers]
  host1

  [app_servers]
  host2
  ```

- Add files to `inventory/group_vars` that correspond to the groups to then specify variables meant for that group e.g.:

  ```yaml
  # postgresql_servers.yml
  pg_version: 10

  # app_db_servers.yml
  app_db_1_name: "db_1"
  app_db_2_name: "db_2"

  # app_servers.yml
  app_version: "1.1.0"
  ```

- You can also condense the variables into a single file (if there are no variable name clashes) by making a super group of your original groups.
  For example you can add the following to `inventory/hosts/app`:

  ```ini
  # app
  # ....

  [app_super_group:children]
  postgresql_servers
  app_db_servers
  app_servers
  ```

  This then allows you to have all the variables inside the file `inventory/group_vars/app_super_group.yml`

### Playbooks:

These compose roles and the hosts they target into a coherent whole. They are the bridge between tasks/roles and hosts.
They are also the files that get *run*.

- Add playbooks files to the `plays` directory
- Playbooks can have multiple hosts definitions in one play.
- Hosts definitions should target groups not individual hosts.
  For example, target the group of hosts that should have postgres installed in them, not an individual host among them.
  The inventory is responsible for assigning hosts to groups. For this reason, use reasonable group names.
- A hosts definition can have multiple role entries.
- Avoid specifying `vars` or `user` in the hosts definitions. Generally, don't have variable values in the playbook itself.
  Those should be either in the role's `defaults/main.yml` or defined by the inventory.
  This limits the source of variable values to command line arguments, inventories or defaults (in order of precedence from highest to lowest).
- Prefer using roles than `pre-tasks` for the same purpose.
- Each hosts definition should have a `name` entry. This aids running and also acts as documentation.
- If the same role is specified multiple times in a host definition, then that role should be parameterized with playbook specific variables otherwise ansible will not run the role more than once.

Here's a simple example of a well defined playbook:

```yaml
---
# app.yml

- hosts: postgresql_servers
  name: Install postgres
  roles:
      - postgresql

- hosts: app_db_servers
  name: Setup databases for the app
  roles:
      - role: pg_db
        pg_db_name: "{{ app_db_1_name }}"

      - role: pg_db
        pg_db_name: "{{ app_db_2_name }}"

- hosts: app_servers
  name: Install the app
  roles:
      - role: app
```

Utilities
---------

First `pip install -r requirements.txt`

**Add a new inventory**

`./run.py create-inventory <inventory_name>`

This will create a dir at `inventories/<inventory_name>` populated with empty dirs for `hosts`, `host_vars` and `group_vars`.

**Add a new role**

`./run.py create-role <role_name>`

This will apply the cookiecutter template at `_templates/role_template` to a new dir at `roles/<role_name>`.
