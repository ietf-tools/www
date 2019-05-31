#!/bin/sh

trap "echo TRAPed signal" HUP INT QUIT TERM

if [ -n "${WWWRUN_UID}" ]; then
  usermod -u "${WWWRUN_UID}" wwwrun
fi

if [ -n "${WWW_GID}" ]; then
  groupmod -g "${WWW_GID}" www
fi

if [ -n "${WWWRUN_UID}" -o -n "${WWW_GID}" ]; then
  chown -R wwwrun:www /code
fi

./mod_wsgi-express-8001/apachectl start

echo "[hit enter key to exit] or run 'docker stop <container>'"
read

./mod_wsgi-express-8001/apachectl stop

echo "exited $0"
