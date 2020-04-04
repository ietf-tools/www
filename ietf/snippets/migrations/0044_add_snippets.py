# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

def forward(apps, schema_editor):
    RFC = apps.get_model('snippets','RFC')
    WorkingGroup = apps.get_model('snippets','WorkingGroup')

    assert(WorkingGroup.objects.filter(acronym='iesg').count()==0)
    assert(RFC.objects.filter(rfc__in=('2434','3932')).count()==0)

    iesg = WorkingGroup.objects.create(
        name = 'Internet Engineering Steering Group',
        acronym = 'iesg',
        list_email = 'iesg@ietf.org',
    )

    WorkingGroup.objects.create(
        name = 'IPv6 over Low power WPAN',
        acronym = '6lowpan',
        list_email = '6lowpan@lists.ietf.org',
        list_subscribe = '6lowpan-request@ietf.org',
    )

    RFC.objects.create(
        rfc='2434',
        name='draft-iesg-iana-considerations',
        title='Guidelines for Writing an IANA Considerations Section in RFCs',
        abstract='This document discusses issues that should be considered in formulating a policy for assigning values to a name space and provides guidelines to document authors on the specific text that must be included in documents that place demands on the IANA.  This document specifies an Internet Best Current Practices for the Internet Community, and requests discussion and suggestions for improvements.',
        working_group = iesg,
    )

    RFC.objects.create(
        rfc='3932',
        name='draft-iesg-rfced-documents',
        title='The IESG and RFC Editor Documents: Procedures',
        abstract="This document describes the IESG's procedures for handling documents submitted for RFC publication via the RFC Editor, subsequent to the changes proposed by the IESG at the Seoul IETF, March 2004.\n\n This document updates procedures described in RFC 2026 and RFC 3710. This document specifies an Internet Best Current Practices for the Internet Community, and requests discussion and suggestions for improvements.",
        working_group = iesg,
    )

def reverse(apps, schema_editor):
    RFC.objects.filter(rfc__in=('2434','3932')).delete()
    WorkingGroup.objects.filter(acronym='iesg').delete()

class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0043_restore_dt_pks_charters'),
    ]

    operations = [
        migrations.RunPython(forward,reverse)
    ]