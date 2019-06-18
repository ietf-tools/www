#!/bin/sh

export DJANGO_SETTINGS_MODULE=ietf.settings.production

sudo -E -u wwwrun ./manage.py migrate
sudo -E -u wwwrun ./manage.py collectstatic --noinput
sudo -E -u wwwrun ./manage.py compress
sudo -E -u wwwrun ./manage.py update_index
