#!/bin/sh

sudo -E -u wwwrun ./manage.py migrate
sudo -E -u wwwrun ./manage.py collectstatic --noinput
sudo -E -u wwwrun ./manage.py compress
sudo -E -u wwwrun ./manage.py update_index_no_datatracker
