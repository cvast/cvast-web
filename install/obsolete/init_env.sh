#!/bin/bash
su postgres --command "/usr/lib/postgresql/9.4/bin/postgres -D /var/lib/postgresql/9.4/main -c config_file=/etc/postgresql/9.4/main/postgresql.conf" &
/elasticsearch/bin/elasticsearch &
sleep 10
python /cvast_web/cvast_arches/manage.py runserver 0.0.0.0:8000