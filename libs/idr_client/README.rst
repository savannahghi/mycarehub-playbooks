Install and Set up IDR Client
=============================

This roles installs and sets up `IDR Client <idr_client_github_page_>`_ on Ubuntu 16.04 LTS, 18.04 LTS and 20.04 LTS hosts.
IDR Client is an ETL(extract, transform and load) tool that extracts data from data sources such as databases and loads the data to a data sink such as the `IDR Server <idr_server_github_page_>`_.
This role should be run on an Ubuntu host that contains data sources with data of interest.

Prerequisites
-------------
For this role to succeed, the following pre-conditions have to be first satisfied/met on the target host.

- A MySQL database server must be installed.
- The `python3-pymsql` package must be installed using the system's package manager.

You will also need to have the `Ansible community MySQL collection <ansible_community_mysql_collection_>`_ installed on the control node. This can be achieved using the following command:

.. code:: bash

    ansible-galaxy collection install community.mysql


.. _ansible_community_mysql_collection: https://galaxy.ansible.com/community/mysql
.. _idr_client_github_page: https://github.com/savannahghi/idr-client
.. _idr_server_github_page: https://github.com/savannahghi/idr-server