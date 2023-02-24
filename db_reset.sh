#!/bin/sh

set -eu
set -o pipefail

echo "Getting backups from ${BACKUPS_BUCKET}"

# basically what happens here is:
# 1. Get the psql binary backup from the bucket
# 2. Ungzip it
# 3. Run pg_restore to turn it into an SQL file
# 4. Insert drop schema to the beginning
# 5. Run the commands in a single transaction and exit on error
# So if anything of the above fails, the database should be left untouched
#aws s3 cp s3://${BACKUPS_BUCKET}/ietfa.torchbox.gz - | gzip -d -c | pg_restore -xO -f - | sed "1s/^/DROP SCHEMA public CASCADE; CREATE SCHEMA public;/" | psql "$DATABASE_URL" -v ON_ERROR_STOP=1 --single-transaction -f -

#python manage.py migrate --noinput

#aws s3 sync --delete s3://${BACKUPS_BUCKET}/media/ s3://${AWS_STORAGE_BUCKET_NAME}/media/

#python manage.py update_nonprod_hostnames
