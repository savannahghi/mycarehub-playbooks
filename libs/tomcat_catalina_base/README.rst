Set up Apache Tomcat CATALINA_BASE
==================================

In `Apache Tomcat <tomcat_home_page_>`_, the ``CATALINA_BASE`` property refers to the root (directory) of a runtime configuration of a specific Tomcat instance. This is important when you want to have multiple Tomcat instances on one machine.
This differs from the ``CATALINA_HOME`` directory which should contains static sources such as ``.jar`` files and/or binary files whereas the ``CATALINA_BASE`` directory should contain configuration files, log files, deployed applications, and other runtime requirements.

This role sets up a ``CATALINA_BASE`` directory and expects that an existing ``CATALINA_HOME`` directory is already present on the target host.

.. note:: 
    This has only been tested on `version 9 <tomcat_9_page_>`_ of Tomcat and might not work with version 10 and above which implement the Jakatra EE specifications. Tomcat 9 and earlier implement specifications developed as part of Java EE.

Prerequisites
-------------
For this role to succeed, the following pre-conditions have to be first satisfied/met on the target host.

- An existing root Tomcat installation as defined by the ``CATALINA_HOME`` property.  *Use the ``tomcat`` role to set this up.*
- A compatible `Java Standard Edition Runtime(JRE) <jre_description_>`_ version for the installed Tomcat version *MUST* present on the target host.


.. _jre_description: https://www.oracle.com/java/technologies/javase/java-runtime-environment.html
.. _tomcat_9_page: https://tomcat.apache.org/tomcat-9.0-doc/introduction.html
.. _tomcat_home_page: https://tomcat.apache.org