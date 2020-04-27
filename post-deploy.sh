#!/bin/sh

sudo --preserve-env=PATH,VIRTUAL_ENV,DJANGO_SETTINGS_MODULE -u wwwrun ./manage.py migrate
sudo --preserve-env=PATH,VIRTUAL_ENV,DJANGO_SETTINGS_MODULE -u wwwrun ./manage.py collectstatic --noinput
sudo --preserve-env=PATH,VIRTUAL_ENV,DJANGO_SETTINGS_MODULE -u wwwrun ./manage.py compress
sudo --preserve-env=PATH,VIRTUAL_ENV,DJANGO_SETTINGS_MODULE -u wwwrun ./manage.py update_index
