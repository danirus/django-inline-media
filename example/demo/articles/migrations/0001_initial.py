# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-18 15:33
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import inline_media.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique_for_date='publish')),
                ('abstract', models.TextField()),
                ('body', inline_media.fields.TextFieldWithInlines()),
                ('publish', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'db_table': 'demo_articles',
                'ordering': ('-publish',),
            },
        ),
    ]