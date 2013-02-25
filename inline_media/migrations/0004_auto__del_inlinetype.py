# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'InlineType'
        db.delete_table('inline_types')


    def backwards(self, orm):
        # Adding model 'InlineType'
        db.create_table('inline_types', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('inline_media', ['InlineType'])


    models = {
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
            'sha1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40', 'db_index': 'True', 'blank': 'True'}),
            'show_as_link': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'show_author': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'show_description_inline': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
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
            'show_counter': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'show_description_inline': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'tags': ('tagging.fields.TagField', [], {'default': "''"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['inline_media']