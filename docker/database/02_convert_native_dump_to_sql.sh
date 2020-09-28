#!/bin/sh

cd /docker-entrypoint-initdb.d

set +e
FILE=$(ls -1 ietfa.torchbox.* | head)

set -e

if [ -s "${FILE}" ]; then
	echo "Found ${FILE}, converting..."
	case $FILE in
		*.gz)
		# -xO means restore no owner, no permissions
		echo "Restoring the gzipped archive..."
		gzip -d -c $FILE | pg_restore -xO -f dump.sql
		;;
		*)
		echo "Restoring the archive..."
		pg_restore -xO -f dump.sql "$FILE"
		;;
	esac
	# schema public is already created
	echo "Hotfixing the dump"
	sed -i -e '/CREATE SCHEMA public/d' dump.sql
else
	echo "No dump, starting fresh."
fi

