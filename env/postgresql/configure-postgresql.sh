#!/bin/bash -xe

/etc/init.d/postgresql start
sudo -u postgres psql --command "CREATE USER payments WITH SUPERUSER PASSWORD 'payments';"
sudo -u postgres psql --command "CREATE DATABASE payments;"
sudo -u postgres psql --command "GRANT ALL PRIVILEGES ON DATABASE payments to payments;"
sudo echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/12/main/pg_hba.conf \
&& echo "listen_addresses='*'" >> /etc/postgresql/12/main/postgresql.conf \
&& /etc/init.d/postgresql restart
