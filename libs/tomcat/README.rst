Install Apache Tomcat on an Ubuntu 20.04 LTS (and above) host
=============================================================

This roles installs an `Apache Tomcat Servlet/JSP Container <tomcat_home_page_>`_ on an Ubuntu 20.04 LTS host and above.
This installation is more suitable for the root installation of Tomcat as defined by the ``CATALINA_HOME`` property. For runtime specific installations (defined by the ``CATALINA_BASE`` property), use the ``tomcat_catalina_base`` role.

.. note::
    This has only been tested on `version 9 <tomcat_9_page_>`_ of Tomcat and might not work with version 10 and above which implement the Jakatra EE specifications. Tomcat 9 and earlier implement specifications developed as part of Java EE.

Prerequisites
-------------

Although not required as part of this installation, it is expected that a compatible `Java Standard Edition Runtime(JRE) <jre_description_>`_ version for the Tomcat version being installed is present on the target host.
The compatible JRE version can be found at the `RUNNING.txt` doc file of the Tomcat version being installed. For example, `here <tomcat_9_running_txt_>`_ is the `RUNNING.txt` for Tomcat version 9.


.. _jre_description: https://www.oracle.com/java/technologies/javase/java-runtime-environment.html
.. _tomcat_9_page: https://tomcat.apache.org/tomcat-9.0-doc/introduction.html
.. _tomcat_9_running_txt: https://tomcat.apache.org/tomcat-9.0-doc/RUNNING.txt
.. _tomcat_home_page: https://tomcat.apache.org