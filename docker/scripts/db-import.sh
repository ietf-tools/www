#!/bin/bash
set -e

echo "Drop dummy app DB if it exists..."
dropdb -U postgres --if-exists app

echo "Import DB dump into app..."
gzip -d -c ietfa.torchbox.latest.gz | pg_restore -xO --clean --if-exists --create -U "$POSTGRES_USER" -d postgres

echo "Done!"