# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Campaign'
        db.create_table('campaign_campaign', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='Campaign Title', max_length=300, null=True)),
            ('start_date_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('end_date_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('code', self.gf('django.db.models.fields.CharField')(default='ABCD', max_length=100, null=True)),
            ('percent', self.gf('django.db.models.fields.IntegerField')(default='50', null=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('chash', self.gf('django.db.models.fields.CharField')(default='', max_length=100, null=True)),
            ('max_people', self.gf('django.db.models.fields.IntegerField')(default='0', null=True, blank=True)),
            ('min_people', self.gf('django.db.models.fields.IntegerField')(default='0', null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('message', self.gf('django.db.models.fields.CharField')(default='50% off admission to Event', max_length=300, null=True)),
            ('message_share', self.gf('django.db.models.fields.CharField')(default='Join me at Event in Las Vegas, Oct 14-16. Use my 50% off coupon.', max_length=300, null=True)),
            ('from_name', self.gf('django.db.models.fields.CharField')(default='Mike', max_length=100, null=True)),
            ('subdomain', self.gf('django.db.models.fields.CharField')(default='www', max_length=50, null=True)),
            ('campaign_type', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
        ))
        db.send_create_signal('campaign', ['Campaign'])

        # Adding M2M table for field admin_access_tusers on 'Campaign'
        db.create_table('campaign_campaign_admin_access_tusers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('campaign', models.ForeignKey(orm['campaign.campaign'], null=False)),
            ('user', models.ForeignKey(orm['tauth.user'], null=False))
        ))
        db.create_unique('campaign_campaign_admin_access_tusers', ['campaign_id', 'user_id'])

        # Adding M2M table for field admin_access_fusers on 'Campaign'
        db.create_table('campaign_campaign_admin_access_fusers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('campaign', models.ForeignKey(orm['campaign.campaign'], null=False)),
            ('fbuser', models.ForeignKey(orm['fauth.fbuser'], null=False))
        ))
        db.create_unique('campaign_campaign_admin_access_fusers', ['campaign_id', 'fbuser_id'])

        # Adding M2M table for field interested_twitter on 'Campaign'
        db.create_table('campaign_campaign_interested_twitter', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('campaign', models.ForeignKey(orm['campaign.campaign'], null=False)),
            ('user', models.ForeignKey(orm['tauth.user'], null=False))
        ))
        db.create_unique('campaign_campaign_interested_twitter', ['campaign_id', 'user_id'])

        # Adding M2M table for field interested_facebook on 'Campaign'
        db.create_table('campaign_campaign_interested_facebook', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('campaign', models.ForeignKey(orm['campaign.campaign'], null=False)),
            ('fbuser', models.ForeignKey(orm['fauth.fbuser'], null=False))
        ))
        db.create_unique('campaign_campaign_interested_facebook', ['campaign_id', 'fbuser_id'])


    def backwards(self, orm):
        
        # Deleting model 'Campaign'
        db.delete_table('campaign_campaign')

        # Removing M2M table for field admin_access_tusers on 'Campaign'
        db.delete_table('campaign_campaign_admin_access_tusers')

        # Removing M2M table for field admin_access_fusers on 'Campaign'
        db.delete_table('campaign_campaign_admin_access_fusers')

        # Removing M2M table for field interested_twitter on 'Campaign'
        db.delete_table('campaign_campaign_interested_twitter')

        # Removing M2M table for field interested_facebook on 'Campaign'
        db.delete_table('campaign_campaign_interested_facebook')


    models = {
        'campaign.campaign': {
            'Meta': {'object_name': 'Campaign'},
            'admin_access_fusers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'admin_access_campaign'", 'to': "orm['fauth.FBUser']"}),
            'admin_access_tusers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'admin_access_campaign'", 'to': "orm['tauth.User']"}),
            'campaign_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'chash': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'default': "'ABCD'", 'max_length': '100', 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'end_date_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'from_name': ('django.db.models.fields.CharField', [], {'default': "'Mike'", 'max_length': '100', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interested_facebook': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'campaign_interested'", 'to': "orm['fauth.FBUser']"}),
            'interested_twitter': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'campaign_interested'", 'to': "orm['tauth.User']"}),
            'max_people': ('django.db.models.fields.IntegerField', [], {'default': "'0'", 'null': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'default': "'50% off admission to Event'", 'max_length': '300', 'null': 'True'}),
            'message_share': ('django.db.models.fields.CharField', [], {'default': "'Join me at Event in Las Vegas, Oct 14-16. Use my 50% off coupon.'", 'max_length': '300', 'null': 'True'}),
            'min_people': ('django.db.models.fields.IntegerField', [], {'default': "'0'", 'null': 'True', 'blank': 'True'}),
            'percent': ('django.db.models.fields.IntegerField', [], {'default': "'50'", 'null': 'True'}),
            'start_date_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'subdomain': ('django.db.models.fields.CharField', [], {'default': "'www'", 'max_length': '50', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'Campaign Title'", 'max_length': '300', 'null': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'fauth.fbuser': {
            'Meta': {'object_name': 'FBUser'},
            'access_token': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '300', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '75', 'blank': 'True'}),
            'facebook_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'profile_pic': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'})
        },
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

    complete_apps = ['campaign']
