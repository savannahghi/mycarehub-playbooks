Install and Set up The OpenMRS EMR
==================================

This role installs The `OpenMRS Platform <openmrs_platform_home_page_>`_ `war` file into an existing Java servlet container instance such as `Apache Tomcat <tomcat_home_page_>`_.

Prerequisites
-------------
For this role to succeed, the following pre-conditions have to be first satisfied/met on the target host.

- An existing Java servlet container instance must be installed and configured.
- A compatible `Java Standard Edition Runtime(JRE) <jre_description_>`_ version for the installed Java server container must be present.
- A MySQL database server must be installed.
- The `python3-pymsql` package must be installed using the system's package manager.

You will also need to have the `Ansible community MySQL collection <ansible_community_mysql_collection_>`_ installed on the control node. This can be achieved using the following command:

.. code:: bash

    ansible-galaxy collection install community.mysql


.. _ansible_community_mysql_collection: https://galaxy.ansible.com/community/mysql
.. _jre_description: https://www.oracle.com/java/technologies/javase/java-runtime-environment.html
.. _openmrs_platform_home_page: https://wiki.openmrs.org/display/docs/OpenMRS+Platform
.. _tomcat_home_page: https://tomcat.apache.org
