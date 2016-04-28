# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-08 12:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=10)),
                ('nationality', models.CharField(max_length=255)),
                ('region', models.CharField(max_length=255)),
                ('occupation', models.CharField(max_length=255)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(choices=[('m', 'male'), ('f', 'female')], max_length=1)),
            ],
        ),
    ]
