# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'User'
        db.create_table('tauth_user', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(default='', max_length=40)),
            ('email', self.gf('django.db.models.fields.EmailField')(default='', max_length=75, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('profile_pic', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('twitter_id', self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(default='', max_length=200, blank=True)),
            ('oauth_token', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('oauth_token_secret', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('tauth', ['User'])


    def backwards(self, orm):
        
        # Deleting model 'User'
        db.delete_table('tauth_user')


    models = {
        'tauth.user': {
            'Meta': {'object_name': 'User'},
            'email': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '75', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'oauth_token': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'oauth_token_secret': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'profile_pic': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'twitter_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40'})
        }
    }

    complete_apps = ['tauth']
