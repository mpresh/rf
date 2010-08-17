# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'FBUser'
        db.create_table('fauth_fbuser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(default='', max_length=80)),
            ('email', self.gf('django.db.models.fields.EmailField')(default='', max_length=75, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('profile_pic', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('facebook_id', self.gf('django.db.models.fields.CharField')(default='', max_length=40, blank=True)),
            ('access_token', self.gf('django.db.models.fields.CharField')(default='', max_length=300, blank=True)),
        ))
        db.send_create_signal('fauth', ['FBUser'])


    def backwards(self, orm):
        
        # Deleting model 'FBUser'
        db.delete_table('fauth_fbuser')


    models = {
        'fauth.fbuser': {
            'Meta': {'object_name': 'FBUser'},
            'access_token': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '300', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '75', 'blank': 'True'}),
            'facebook_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'profile_pic': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'})
        }
    }

    complete_apps = ['fauth']
