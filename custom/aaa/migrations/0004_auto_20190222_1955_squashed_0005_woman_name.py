# -*- coding: utf-8 -*-
# flake8: noqa
# Generated by Django 1.11.20 on 2019-02-22 22:29
from __future__ import absolute_import
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aaa', '0003_auto_20190215_1938_squashed_0004_auto_20190215_2103'),
    ]

    operations = [
        migrations.AddField(
            model_name='child',
            name='mother_case_id',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='woman',
            name='age_marriage',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='woman',
            name='contact_phone_number',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='woman',
            name='has_aadhar_number',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='woman',
            name='hh_address',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='woman',
            name='hh_bpl_apl',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='woman',
            name='hh_caste',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='woman',
            name='hh_religion',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='woman',
            name='husband_name',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='woman',
            name='num_female_children_died',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='woman',
            name='num_male_children_died',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='womanhistory',
            name='family_planning_form_history',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.DateField(), help_text='timeEnd from Family Planning forms submitted against this case', null=True, size=None),
        ),
        migrations.AddField(
            model_name='woman',
            name='name',
            field=models.TextField(null=True),
        ),
    ]
