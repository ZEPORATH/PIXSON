# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-11 12:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resizer', '0008_opencv'),
    ]

    operations = [
        migrations.CreateModel(
            name='Opencv2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height', models.CharField(help_text='Enter height in px', max_length=100)),
                ('width', models.CharField(help_text='Enter width in px', max_length=100)),
                ('resize_method', models.CharField(help_text='Enter method for resizing', max_length=255)),
            ],
        ),
    ]
