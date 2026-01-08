#!/usr/bin/env bash
# start-server.sh
cd /tmp/app/eccr-cis/app
# python manage.py waitdb
python3 manage.py collectstatic --no-input
python3 manage.py migrate
python3 manage.py createcachetable
cp -ur ./static/ /tmp/shared/
./start-server.sh
