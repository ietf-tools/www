#!/bin/bash

. /usr/local/bin/docker-entrypoint.sh

cd /docker-entrypoint-initdb.d

set +e
FILE=$(ls -1 ietfa.*.gz | head)

set -e

restore_dump() {
	# use docker_process_sql function from docker-entrypoint.sh in the Postgres container
	# pg_restore -xO means restore no owner, no permissions
	pg_restore -xO -f - | sed -e '/CREATE SCHEMA public/d' | docker_process_sql
}

if [ -s "${FILE}" ]; then
	echo "Found ${FILE}, converting..."
	case $FILE in
		*.gz)
		echo "Restoring the gzipped archive..."
		gzip -d -c $FILE | restore_dump
		;;
		*)
		echo "Restoring the archive..."
		cat $FILE | restore_dump
		;;
	esac
else
	echo "No dump, starting fresh."
fi

