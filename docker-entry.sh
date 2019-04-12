#!/bin/sh

trap "echo TRAPed signal" HUP INT QUIT TERM

sudo -E -u wwwrun ./manage.py migrate
sudo -E -u wwwrun ./manage.py collectstatic --noinput
sudo -E -u wwwrun ./manage.py update_index_no_datatracker

./mod_wsgi-express-8001/apachectl start

echo "[hit enter key to exit] or run 'docker stop <container>'"
read

./mod_wsgi-express-8001/apachectl stop

echo "exited $0"
