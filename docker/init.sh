#!/bin/bash

echo "Running management commands..."
. deploy.sh

echo "Starting supervisor..."
/usr/bin/supervisord -c /app/supervisord.conf
