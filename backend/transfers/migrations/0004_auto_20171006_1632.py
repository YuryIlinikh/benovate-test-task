# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-06 16:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transfers', '0003_auto_20171006_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inn',
            name='inn',
            field=models.BigIntegerField(max_length=12, unique=True),
        ),
    ]
