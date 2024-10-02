#!/bin/bash

. /usr/local/bin/docker-entrypoint.sh

cd /docker-entrypoint-initdb.d

set +e
FILE=$(ls -1 *.dump | head)

set -e

restore_dump() {
    # use docker_process_sql function from docker-entrypoint.sh in the Postgres container
    # pg_restore -xO means restore no owner, no permissions
    cat "$1" | pg_restore -xO  -f - | sed -e '/CREATE SCHEMA public/d' | docker_process_sql
}

if [ -s "${FILE}" ]; then
    echo "Restoring the archive..."
    restore_dump "$FILE"
else
    echo "No dump, starting fresh."
fi

