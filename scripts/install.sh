#!/bin/bash
gitDir="/home/kevin/ansible"

sudo apt-get update && sudo apt-get dist-upgrade -y
sudo apt-get install python3-pip ansible -y
#python3 -m pip install --user kevin
sudo cp -R $gitDir/ansible-files/* /etc/ansible