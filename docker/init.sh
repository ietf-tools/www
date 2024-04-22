#!/bin/bash

echo "Running migrate..."
python /app/manage.py migrate

echo "Starting supervisor..."
/usr/bin/supervisord -c /app/supervisord.conf
