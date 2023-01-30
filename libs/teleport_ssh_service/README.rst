Install and Set up an Ubuntu Host with the Teleport SSH Service
===============================================================

This role installs `Teleport <teleport_docs_>`_ on an Ubuntu host and configures and activates the `Teleport SSH Service <teleport_server_access_docs_>`_.

.. note:: 
    Internally, this role uses the `teleport` role but overrides certain variables in order to set up the Teleport SSH Service.
    This role will only set up the Teleport SSH service and no other Teleport service and thus is not suitable for scenarios where multiple Teleport services are required.
    It should also be noted that this role will overwrite any existing Teleport config on the target host.


Prerequisites
-------------
This role requires that a running Teleport Cluster already exists. See details on how to do that `here <teleport_tutorial_introduction_docs_>`_.
You will also need to have sufficient permission and access to the Teleport cluster. This is required to generate a cluster join token needed to add nodes to the target cluster.

Get the Join Token
~~~~~~~~~~~~~~~~~~
To get the join token:

- First login into the cluster and then open a terminal. Alternatively, if you have Teleport installed on your machine, you can login to the cluster using `tsh` and then use the `tctl` remotely.
- Once you are logged in, run the following command to generate the token:

    .. code:: bash

        sudo tctl tokens add --type=node --format=json --ttl=1h
  
  The token is the value of the ``token`` key on the displayed json.

  The ``--ttl`` argument specifies the duration for which the token will be valid. The value ``1h`` specifies that the token will be valid for 1 hour.

That's it, you are good to go.

.. _teleport_docs: https://goteleport.com/docs
.. _teleport_tutorial_introduction_docs: https://goteleport.com/docs/try-out-teleport/introduction
.. _teleport_server_access_docs: https://goteleport.com/docs/server-access/introduction
