# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Purpose'
        db.create_table(u'servers_purpose', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('purpose_website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'servers', ['Purpose'])

        # Adding M2M table for field purposes on 'Server'
        m2m_table_name = db.shorten_name(u'servers_server_purposes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('server', models.ForeignKey(orm[u'servers.server'], null=False)),
            ('purpose', models.ForeignKey(orm[u'servers.purpose'], null=False))
        ))
        db.create_unique(m2m_table_name, ['server_id', 'purpose_id'])


    def backwards(self, orm):
        # Deleting model 'Purpose'
        db.delete_table(u'servers_purpose')

        # Removing M2M table for field purposes on 'Server'
        db.delete_table(db.shorten_name(u'servers_server_purposes'))


    models = {
        u'servers.extra_ip': {
            'Meta': {'object_name': 'Extra_IP'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['servers.Server']"})
        },
        u'servers.purpose': {
            'Meta': {'object_name': 'Purpose'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'purpose_website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'servers.server': {
            'Meta': {'object_name': 'Server'},
            'bandwidth': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'billing_type': ('django.db.models.fields.CharField', [], {'default': "'m'", 'max_length': '1'}),
            'burst': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'check_status': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '2'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'hdd_space': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'number_cores': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'purchased_at': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'purposes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['servers.Purpose']", 'symmetrical': 'False'}),
            'ram': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'virt_type': ('django.db.models.fields.CharField', [], {'default': "'o'", 'max_length': '1'})
        },
        u'servers.servercheck': {
            'Meta': {'object_name': 'ServerCheck'},
            'check_date': ('django.db.models.fields.DateTimeField', [], {}),
            'did_change': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'last_change': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['servers.ServerCheck']", 'null': 'True', 'blank': 'True'}),
            'online': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['servers.Server']"})
        }
    }

    complete_apps = ['servers']