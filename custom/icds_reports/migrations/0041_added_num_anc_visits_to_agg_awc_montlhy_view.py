# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-13 9:25
from __future__ import absolute_import
from __future__ import unicode_literals

from django.db import migrations
from corehq.sql_db.operations import RawSQLMigration

migrator = RawSQLMigration(('custom', 'icds_reports', 'migrations', 'sql_templates'))


class Migration(migrations.Migration):

    dependencies = [
        ('icds_reports', '0040_add_days_ration_column'),
    ]

    operations = [
        migrator.get_migration('create_datasource_views.sql'),
    ]