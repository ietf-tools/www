from django.core.management.base import BaseCommand

import datetime
import pytz

from django.db import connection, transaction

class Command(BaseCommand):
    help = 'Assault the django_migrations table and convince it the current 0001_initial migrations are all there are for the ietf apps, and that they were applied today'

    def handle(self, *args, **options):

        now = pytz.utc.localize(datetime.datetime.utcnow())

        cursor = connection.cursor()

        cursor.execute("delete from django_migrations where app='datatracker'")
        transaction.commit()

        for app in ('blog','documents','events','forms','glossary','home','iesg_statement','images','snippets','standard','topics','utils'):

            cursor.execute("delete from django_migrations where app='%s' and name!='0001_initial'" % app)
            cursor.execute("update django_migrations set applied='%s' where app='%s' and name='0001_initial'" % (now, app))
            transaction.commit()

