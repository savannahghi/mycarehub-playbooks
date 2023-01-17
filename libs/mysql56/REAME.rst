Install MySQL 5.6 on Ubuntu 20.04 LTS (and above)
=================================================

This role installs MySQL 5.6 on an Ubuntu 20.04 host and above.

.. note::
    If this is a first time install, i.e the variable ``mysql56_is_fresh_install`` is set to ``true``, ensure that the MySQL 5.6 Server (if one exists) on the host is shutdown, otherwise this role will fail.
