# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-09 13:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionsource', '0002_auto_20170509_1231'),
    ]

    operations = [
        migrations.CreateModel(
            name='CollecteData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, default='', max_length=100)),
                ('xpath', models.CharField(blank=True, default='', max_length=100)),
                ('appID', models.CharField(blank=True, default='', max_length=100)),
                ('appSecret', models.CharField(blank=True, default='', max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
    ]
