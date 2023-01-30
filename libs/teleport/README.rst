Install and Configure Teleport on an Ubuntu Host
================================================

This role installs `Teleport <teleport_docs_>`_ and provides variables to override specific parts of the `configuration <teleport_config_reference_>`_ to suite the installation context.
That is, with this role and proper overriding of the configuration, Teleport can be installed and configured to provide any or all of it's services such as the The Teleport Auth Service, Teleport SSH Service and more.

.. note:: 
    By default, the installed Teleport binary will not be configured to do anything useful and in fact, the Teleport ``systemd`` is not even started.
    It's up to the clients/users of this role to provide the proper configuration overrides as per the installation context.

.. _teleport_config_reference: https://goteleport.com/docs/reference/config
.. _teleport_docs: https://goteleport.com/docs
