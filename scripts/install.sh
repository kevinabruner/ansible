#!/bin/bash
gitDir="/home/kevin/ansible"

sudo apt-get update && sudo apt-get dist-upgrade -y
sudo apt-get install ansible -y
sudo cp -R $gitDir/ansible-files/* /etc/ansible