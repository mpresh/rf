# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'AttributeType'
        db.create_table('entities_attributetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='STRING', max_length=100)),
            ('allowed_values', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=300, null=True)),
        ))
        db.send_create_signal('entities', ['AttributeType'])

        # Adding model 'Attribute'
        db.create_table('entities_attribute', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entities.AttributeType'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('value', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
        ))
        db.send_create_signal('entities', ['Attribute'])

        # Adding model 'EntityType'
        db.create_table('entities_entitytype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('entities', ['EntityType'])

        # Adding M2M table for field required_fields on 'EntityType'
        db.create_table('entities_entitytype_required_fields', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('entitytype', models.ForeignKey(orm['entities.entitytype'], null=False)),
            ('attributetype', models.ForeignKey(orm['entities.attributetype'], null=False))
        ))
        db.create_unique('entities_entitytype_required_fields', ['entitytype_id', 'attributetype_id'])

        # Adding M2M table for field allowed_fields on 'EntityType'
        db.create_table('entities_entitytype_allowed_fields', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('entitytype', models.ForeignKey(orm['entities.entitytype'], null=False)),
            ('attributetype', models.ForeignKey(orm['entities.attributetype'], null=False))
        ))
        db.create_unique('entities_entitytype_allowed_fields', ['entitytype_id', 'attributetype_id'])

        # Adding model 'Entity'
        db.create_table('entities_entity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['entities.EntityType'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('entities', ['Entity'])

        # Adding M2M table for field fields on 'Entity'
        db.create_table('entities_entity_fields', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('entity', models.ForeignKey(orm['entities.entity'], null=False)),
            ('attribute', models.ForeignKey(orm['entities.attribute'], null=False))
        ))
        db.create_unique('entities_entity_fields', ['entity_id', 'attribute_id'])


    def backwards(self, orm):
        
        # Deleting model 'AttributeType'
        db.delete_table('entities_attributetype')

        # Deleting model 'Attribute'
        db.delete_table('entities_attribute')

        # Deleting model 'EntityType'
        db.delete_table('entities_entitytype')

        # Removing M2M table for field required_fields on 'EntityType'
        db.delete_table('entities_entitytype_required_fields')

        # Removing M2M table for field allowed_fields on 'EntityType'
        db.delete_table('entities_entitytype_allowed_fields')

        # Deleting model 'Entity'
        db.delete_table('entities_entity')

        # Removing M2M table for field fields on 'Entity'
        db.delete_table('entities_entity_fields')


    models = {
        'entities.attribute': {
            'Meta': {'object_name': 'Attribute'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['entities.AttributeType']"}),
            'value': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'})
        },
        'entities.attributetype': {
            'Meta': {'object_name': 'AttributeType'},
            'allowed_values': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'STRING'", 'max_length': '100'})
        },
        'entities.entity': {
            'Meta': {'object_name': 'Entity'},
            'fields': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['entities.Attribute']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['entities.EntityType']"})
        },
        'entities.entitytype': {
            'Meta': {'object_name': 'EntityType'},
            'allowed_fields': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'entities_allow'", 'blank': 'True', 'to': "orm['entities.AttributeType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'required_fields': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'entities_require'", 'blank': 'True', 'to': "orm['entities.AttributeType']"})
        }
    }

    complete_apps = ['entities']
