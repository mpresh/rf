# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Share.created_at'
        db.alter_column('events_share', 'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True))


    def backwards(self, orm):
        
        # Changing field 'Share.created_at'
        db.alter_column('events_share', 'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))


    models = {
        'campaign.campaign': {
            'Meta': {'object_name': 'Campaign'},
            'admin_access_fusers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'admin_access_campaign'", 'to': "orm['fauth.FBUser']"}),
            'admin_access_tusers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'admin_access_campaign'", 'to': "orm['tauth.User']"}),
            'campaign_type': ('django.db.models.fields.CharField', [], {'default': "'discount'", 'max_length': '50'}),
            'chash': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'default': "'ABCD'", 'max_length': '100', 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'end_date_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'facebook_fan_page': ('django.db.models.fields.CharField', [], {'default': "'RippleFunction'", 'max_length': '300', 'null': 'True'}),
            'from_name': ('django.db.models.fields.CharField', [], {'default': "'Mike'", 'max_length': '100', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interested_facebook': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'campaign_interested'", 'to': "orm['fauth.FBUser']"}),
            'interested_twitter': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'campaign_interested'", 'to': "orm['tauth.User']"}),
            'max_people': ('django.db.models.fields.IntegerField', [], {'default': "'0'", 'null': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'default': "'50% off admission to Event'", 'max_length': '300', 'null': 'True'}),
            'message_share': ('django.db.models.fields.CharField', [], {'default': "'Join me at Event in Las Vegas, Oct 14-16. Use my 50% off coupon.'", 'max_length': '300', 'null': 'True'}),
            'min_people': ('django.db.models.fields.IntegerField', [], {'default': "'0'", 'null': 'True', 'blank': 'True'}),
            'page_views': ('django.db.models.fields.IntegerField', [], {'default': "'0'"}),
            'page_views_total': ('django.db.models.fields.IntegerField', [], {'default': "'0'"}),
            'percent': ('django.db.models.fields.IntegerField', [], {'default': "'50'", 'null': 'True'}),
            'start_date_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'subdomain': ('django.db.models.fields.CharField', [], {'default': "'www'", 'max_length': '50', 'null': 'True'}),
            'template': ('django.db.models.fields.IntegerField', [], {'default': "'0'", 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'Campaign Title'", 'max_length': '300', 'null': 'True'}),
            'twitter_account': ('django.db.models.fields.CharField', [], {'default': "'RippleFunction'", 'max_length': '300', 'null': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'url_redeem': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'events.event': {
            'Meta': {'object_name': 'Event'},
            'attendees': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'events_going'", 'to': "orm['tauth.User']"}),
            'attendees_maybe': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'events_maybe'", 'to': "orm['tauth.User']"}),
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'events'", 'null': 'True', 'to': "orm['campaign.Campaign']"}),
            'capacity': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'ehash': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True'}),
            'event_date_time_end': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'event_date_time_start': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '4', 'blank': 'True'}),
            'lng': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '4', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'organizer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'events_organized'", 'null': 'True', 'to': "orm['tauth.User']"}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'venue': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'venue_address': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'})
        },
        'events.share': {
            'Meta': {'object_name': 'Share'},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'shares'", 'null': 'True', 'to': "orm['campaign.Campaign']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invites'", 'null': 'True', 'to': "orm['events.Event']"}),
            'from_account_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'from_invite': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'child_invites'", 'null': 'True', 'to': "orm['events.Share']"}),
            'from_user_facebook': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'made_invites_facebook'", 'null': 'True', 'to': "orm['fauth.FBUser']"}),
            'from_user_twitter': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'made_invites_twitter'", 'null': 'True', 'to': "orm['tauth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '140'}),
            'page_views': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent_shash': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True'}),
            'reach': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'shash': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True'}),
            'url_full': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'null': 'True'}),
            'url_short': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'null': 'True'})
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

    complete_apps = ['events']
