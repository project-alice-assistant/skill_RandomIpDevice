#!/usr/bin/env bash

echo 'net.ipv4.ping_group_range = ' $UID $UID | sudo tee -a /etc/sysctl.conf
