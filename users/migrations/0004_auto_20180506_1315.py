# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-05-06 13:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20180502_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlists',
            name='albumart',
            field=models.CharField(default='https://yt3.ggpht.com/pHwZj3tkgC3SJFbuqebBoT7WtVcIwAijEmcbe9VDCauv9ZlG6uS2zjvZQUSO7SfFqa3xjYqGp_L4QbM7=s900-mo-c-c0xffffffff-rj-k-no', max_length=200),
        ),
    ]
