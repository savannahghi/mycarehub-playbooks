Install Eclipse Jetty Server on an Ubuntu 20.04 LTS (and above) host
====================================================================

This role installs an `Eclipse Jetty Server <jetty_server_home_page_>`_ on an Ubuntu 20.04 LTS host and above.
This installation is more suitable for the root installation of Jetty as defined by the ``JETTY_HOME`` property. For runtime specific installations (defined by the ``JETTY_BASE`` property), use the ``jetty_base`` role. See `here <jetty_server_quick_start_docs_>`_ for more details.


Prerequisites
-------------

Although not performed as part of this installation, it is expected that a compatible `Java Standard Edition Runtime(JRE) <jre_description_>`_ version for the Eclipse Jetty version being installed is present on the target host.
The compatible JRE version can be found at the `Jetty Versions` section of `this <jetty_server_download_page_>`_ page.

Role Defaults
-------------

+---------------------+-----------------------------+
| Attribute Name      | Default Value               |
+=====================+=============================+
| common tag          | jetty_home                  |
+---------------------+-----------------------------+
| variable prefix     | ``jetty_``                  |
+---------------------+-----------------------------+

- **common tag:** This attribute refers to the tag shared across all tasks in this role.
- **variable prefix:** This attribute refers to a string that is prepended to all variable names used by this role.

.. _jetty_server_download_page: https://www.eclipse.org/jetty/download.php
.. _jetty_server_home_page: https://www.eclipse.org/jetty
.. _jetty_server_quick_start_docs: https://www.eclipse.org/jetty/documentation/jetty-12/operations-guide/index.html#og-quick-setup
.. _jre_description: https://www.oracle.com/java/technologies/javase/java-runtime-environment.html
