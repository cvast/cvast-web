# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-18 18:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_paragraph'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsindexpage',
            name='back_button',
            field=models.CharField(default='Back to News Overview', max_length=40),
        ),
        migrations.AddField(
            model_name='newstagindexpage',
            name='back_button',
            field=models.CharField(default='Back to Tag Overview', max_length=40),
        ),
    ]