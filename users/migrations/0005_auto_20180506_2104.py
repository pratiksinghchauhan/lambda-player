# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-05-06 21:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20180506_1315'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='playlistsongs',
            options={'ordering': ['position', 'pk']},
        ),
        migrations.AddField(
            model_name='playlistsongs',
            name='position',
            field=models.IntegerField(default=0),
        ),
    ]