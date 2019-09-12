#!/bin/sh

trap "echo TRAPed signal" HUP INT QUIT TERM

if [ -n "${WWWRUN_UID}" ]; then
  usermod -u "${WWWRUN_UID}" wwwrun
fi

if [ -n "${WWW_GID}" ]; then
  groupmod -g "${WWW_GID}" www
fi

if [ ! -f "ietf/settings/local.py" ]; then
    echo "local.py not found. Exiting."
    exit 1
fi

if [ ! -d "mod_wsgi-express-8001" ]; then
    echo "mod_wsgi-express-8001 not found. Exiting."
    exit 1
fi

./mod_wsgi-express-8001/apachectl start

echo "Successfully started. [hit enter key to exit] or run 'docker stop <container>'"
read

./mod_wsgi-express-8001/apachectl stop

echo "exited $0"
