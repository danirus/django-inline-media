# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'InlineType'
        db.create_table('inline_types', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
        ))
        db.send_create_signal('inline_media', ['InlineType'])

        # Adding model 'License'
        db.create_table('inline_media_licenses', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('link', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
            ('tags', self.gf('tagging.fields.TagField')(default='')),
        ))
        db.send_create_signal('inline_media', ['License'])

        # Adding model 'Picture'
        db.create_table('inline_media_pictures', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('show_as_link', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('picture', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('tags', self.gf('tagging.fields.TagField')(default='')),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('show_author', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('license', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inline_media.License'], null=True, blank=True)),
            ('show_license', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('uploaded', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('sha1', self.gf('django.db.models.fields.CharField')(default='', max_length=40, blank=True)),
        ))
        db.send_create_signal('inline_media', ['Picture'])

        # Adding model 'PictureSet'
        db.create_table('inline_media_picture_sets', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('tags', self.gf('tagging.fields.TagField')(default='')),
            ('cover', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inline_media.Picture'], null=True, blank=True)),
            ('order', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=512, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('inline_media', ['PictureSet'])

        # Adding M2M table for field pictures on 'PictureSet'
        db.create_table('inline_media_picture_sets_pictures', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pictureset', models.ForeignKey(orm['inline_media.pictureset'], null=False)),
            ('picture', models.ForeignKey(orm['inline_media.picture'], null=False))
        ))
        db.create_unique('inline_media_picture_sets_pictures', ['pictureset_id', 'picture_id'])


    def backwards(self, orm):
        # Deleting model 'InlineType'
        db.delete_table('inline_types')

        # Deleting model 'License'
        db.delete_table('inline_media_licenses')

        # Deleting model 'Picture'
        db.delete_table('inline_media_pictures')

        # Deleting model 'PictureSet'
        db.delete_table('inline_media_picture_sets')

        # Removing M2M table for field pictures on 'PictureSet'
        db.delete_table('inline_media_picture_sets_pictures')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'inline_media.inlinetype': {
            'Meta': {'object_name': 'InlineType', 'db_table': "'inline_types'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'inline_media.license': {
            'Meta': {'object_name': 'License', 'db_table': "'inline_media_licenses'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tags': ('tagging.fields.TagField', [], {'default': "''"})
        },
        'inline_media.picture': {
            'Meta': {'ordering': "('-uploaded',)", 'object_name': 'Picture', 'db_table': "'inline_media_pictures'"},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'license': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inline_media.License']", 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'picture': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100'}),
            'sha1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40', 'blank': 'True'}),
            'show_as_link': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'show_author': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'show_license': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tags': ('tagging.fields.TagField', [], {'default': "''"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'uploaded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'inline_media.pictureset': {
            'Meta': {'object_name': 'PictureSet', 'db_table': "'inline_media_picture_sets'"},
            'cover': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inline_media.Picture']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '512', 'blank': 'True'}),
            'pictures': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'picture_sets'", 'symmetrical': 'False', 'to': "orm['inline_media.Picture']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'tags': ('tagging.fields.TagField', [], {'default': "''"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['inline_media']