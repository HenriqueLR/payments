#!/bin/bash -xe

apt-get install -y sudo && sudo apt-get -y update \
&& ./env/sys/add-user.sh \
&& apt-get install -y netcat \
&& pip install -r ./requirements.txt \
&& rm -rf /var/lib/apt/lists/* && apt-get clean
