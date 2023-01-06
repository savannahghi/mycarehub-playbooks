#!/bin/bash

export CATALINA_HOME="{{ catalina_base_tomcat_root_dir }}"
export CATALINA_BASE="{{ catalina_base_root_dir }}"

export JAVA_HOME="{{ catalina_base_java_home }}"
export JAVA_OPTS="-Xmx{{ catalina_base_maximum_java_heap_size }} -Xms{{ catalina_base_initial_java_heap_size }} -Djava.awt.headless=true"
