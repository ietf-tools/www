#!/bin/bash

echo "Running collectstatic..."
python /app/manage.py collectstatic --no-input

echo "Starting supervisor..."
/usr/bin/supervisord -c /app/supervisord.conf
