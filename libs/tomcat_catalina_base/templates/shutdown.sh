#!/bin/bash

# Set environment variables
source {{ catalina_base_root_dir }}/bin/setenv.sh

# Stop Tomcat
{{ catalina_base_tomcat_root_dir }}/bin/shutdown.sh

echo "Tomcat stopped"
# Set environment variables
source {{ catalina_base_root_dir }}/bin/setenv.sh

# Startup Tomcat
{{ catalina_base_tomcat_root_dir }}/bin/startup.sh

echo "Tomcat started ;)"
