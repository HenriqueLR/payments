#!/bin/bash -xe

groupadd supersudo && echo "%supersudo ALL=(ALL:ALL) NOPASSWD: ALL" > /etc/sudoers.d/supersudo
adduser --disabled-password --gecos payments payments && usermod -a -G supersudo payments && mkdir -p /home/payments/.ssh
echo -e "Host github.com\n\tStrictHostKeyChecking no\n" > /home/payments/.ssh/config
sudo chown -R payments:payments /home/payments
sudo chmod 600 /home/payments/.ssh/*