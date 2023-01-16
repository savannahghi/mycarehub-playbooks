Install and set up Chai WebADT on an Ubuntu 20.04 LTS server
============================================================

This role installs and sets up the `Chai WebADT EMR <chai_webADT_linux_wiki_>`_ on an Ubuntu 20.04 LTS server.

Prerequisites
-------------

For this role to succeed, the following pre-conditions have to be first satisfied/met on the target host.

- PHP 7.4 must be installed.
- A MySQL database server must be installed.
- The `python3-pymsql` package must be installed using the system's package manager.

You will also need to have the `Ansible community MySQL collection <ansible_community_mysql_collection_>`_ installed on the control node. This can be achieved using the following command:

.. code:: bash

    ansible-galaxy collection install community.mysql


.. _ansible_community_mysql_collection: https://galaxy.ansible.com/community/mysql
.. _chai_webADT_linux_wiki: https://bitbucket.org/chaike/adtv4/wiki/Ubuntu%20Installation
