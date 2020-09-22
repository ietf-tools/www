#!/bin/sh

cd /docker-entrypoint-initdb.d

FILE=$(ls -1 ietfa.torchbox.* | head)
if [ -s "${FILE}" ]; then
	echo "Found ${FILE}, converting..."
	# no owner, no permissions
	pg_restore -xO -f dump.sql "$FILE"
	echo "hotfixing the dump"
	sed -i -e '/CREATE SCHEMA public/d' dump.sql
else
	echo "no dump, failing"
	exit 1
fi

