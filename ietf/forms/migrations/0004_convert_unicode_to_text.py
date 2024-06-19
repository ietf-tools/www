from django.db import migrations, models


def convert_unicode_to_text(apps, schema_editor):
    if apps.is_installed("wagtailforms"):
        Submissions = apps.get_model("wagtailforms", "formsubmission")
        for submission in Submissions.objects.all():
            submission.form_data = str(submission.form_data.replace("\\u0000", ""))
            submission.save()


class Migration(migrations.Migration):

    dependencies = [
        ("forms", "0003_auto_20220722_0302"),
    ]

    operations = [migrations.RunPython(convert_unicode_to_text)]
