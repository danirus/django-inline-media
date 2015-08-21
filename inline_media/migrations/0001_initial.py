# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields
import taggit.managers
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=255)),
                ('link', models.URLField(unique=True)),
                ('tags', taggit.managers.TaggableManager(through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags', to='taggit.Tag')),
            ],
            options={
                'db_table': 'inline_media_licenses',
            },
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=255)),
                ('picture', sorl.thumbnail.fields.ImageField(storage=django.core.files.storage.FileSystemStorage(), upload_to='pictures/%Y/%b/%d')),
                ('show_as_link', models.BooleanField(default=True)),
                ('description', models.TextField(blank=True)),
                ('show_description_inline', models.BooleanField(default=True, verbose_name='Show description inline')),
                ('author', models.CharField(help_text="picture's author", max_length=255, blank=True)),
                ('show_author', models.BooleanField(default=False)),
                ('show_license', models.BooleanField(default=False)),
                ('uploaded', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('sha1', models.CharField(blank=True, default='', db_index=True, max_length=40)),
                ('license', models.ForeignKey(null=True, to='inline_media.License', blank=True)),
                ('tags', taggit.managers.TaggableManager(through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags', to='taggit.Tag')),
            ],
            options={
                'db_table': 'inline_media_pictures',
                'ordering': ('-uploaded',),
            },
        ),
        migrations.CreateModel(
            name='PictureSet',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('title', models.CharField(help_text="Visible at the top of the gallery slider that shows up when clicking on cover's picture.", max_length=255)),
                ('slug', models.SlugField()),
                ('description', models.TextField(help_text='Only visible in the inline under sizes small, medium, large or full.', blank=True)),
                ('show_description_inline', models.BooleanField(default=True)),
                ('order', models.CommaSeparatedIntegerField(help_text='Establish pictures order by typing the comma separated list of their picture IDs.', max_length=512, blank=True)),
                ('show_counter', models.BooleanField(help_text='Whether to show how many pictures contains the pictureset.', default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('pictures', models.ManyToManyField(related_name='picture_sets', to='inline_media.Picture')),
                ('tags', taggit.managers.TaggableManager(through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags', to='taggit.Tag')),
            ],
            options={
                'db_table': 'inline_media_picture_sets',
            },
        ),
    ]
