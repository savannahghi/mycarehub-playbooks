
Install Apache HTTP Server on an Ubuntu 20.04 LTS (and above) host
==================================================================

This role installs an `Apache HTTP Server <apache_server_home_page_>`_ on an Ubuntu 20.04 LTS host and above.

.. note::
    - This role differs from the normal ``apt`` install of Apache in that it sets up a separate "instance" (different ``ServerRoot`` and configuration) of the server and allows for the new instance to be run by a different user other than root.
    - By default after a successful installation, this role shutdowns and disables the default Apache service instance started by apt at installation (typically named ``apache2.service``) if already running. This can be disabled by setting the variable ``apache_httpd_stop_default_apache_service`` to ``false``.

.. _apache_server_home_page: https://httpd.apache.org
