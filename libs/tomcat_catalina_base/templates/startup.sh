#!/bin/bash

# Ensure we are running as the appropriate user
if [[ `id -nu` != "{{ catalina_base_owning_user }}" ]]; then
   echo "Not running as {{ catalina_base_owning_user }}, exiting.."
   exit 1
fi

# Startup Tomcat
{{ catalina_base_tomcat_root_dir }}/bin/startup.sh

echo "Tomcat started ;)"
