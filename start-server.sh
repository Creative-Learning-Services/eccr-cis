#!/usr/bin/env bash
# start-server.sh
cd /tmp/app/eccr-cis/app
(gunicorn CIS.wsgi --reload --user python --bind 0.0.0.0:8020 --workers 3)
