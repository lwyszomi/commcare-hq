# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-27 15:01
from __future__ import unicode_literals

from django.db import migrations

from corehq.sql_db.operations import RawSQLMigration

migrator = RawSQLMigration(('custom', 'icds_reports', 'migrations', 'sql_templates'))


class Migration(migrations.Migration):

    dependencies = [
        ('icds_reports', '0026_add_map_location_name'),
    ]

    operations = [
    ]
