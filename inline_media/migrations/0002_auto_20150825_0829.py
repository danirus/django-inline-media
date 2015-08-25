# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('inline_media', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='license',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, verbose_name='Tags', to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.'),
        ),
        migrations.AlterField(
            model_name='picture',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, verbose_name='Tags', to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.'),
        ),
        migrations.AlterField(
            model_name='pictureset',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, verbose_name='Tags', to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.'),
        ),
    ]
