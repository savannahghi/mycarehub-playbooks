#!/bin/bash

# This will ensure that the logs folder ({{ idr_client_logs_dir }}) is always writable
#  by the application user group ({{ idr_client_user_group }}) regardless of the umask
#  config of the executing user.
umask 0005
{{ idr_client_installation_dir }}/idr_client -c {{ idr_client_config_dir }}/config.yml 

