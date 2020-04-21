# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-11-24 20:52
from __future__ import unicode_literals

from django.db import migrations, transaction


def copy_column_value_forwards(apps, schema_editor):
    """
    Copy the start field into start_date field

    This table has around 25 million rows, we'll follow non-atomic migrations.
    https://docs.djangoproject.com/en/2.2/howto/writing-migrations/#non-atomic-migrations
    """
    Schedule = apps.get_model('schedules', 'Schedule')
    while Schedule.objects.filter(start_date__isnull=True).exists():
        with transaction.atomic():
            for row in Schedule.objects.filter(start_date__isnull=True)[:1000]:
                row.start_date = row.start
                row.save()


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('schedules', '0008_add_new_start_date_field'),
    ]

    operations = [
        migrations.RunPython(
            copy_column_value_forwards,
            reverse_code=migrations.RunPython.noop,  # Allow reverse migrations, but make it a no-op.
        )
    ]
