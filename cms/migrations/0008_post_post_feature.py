# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-14 18:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0007_externalurls'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_feature',
            field=models.CharField(default='#', max_length=255),
        ),
    ]
