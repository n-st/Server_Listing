# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        db.alter_column(u'servers_server', 'bandwidth', self.gf('django.db.models.fields.BigIntegerField')())
        db.alter_column(u'servers_server', 'burst', self.gf('django.db.models.fields.BigIntegerField')())
        db.alter_column(u'servers_server', 'hdd_space', self.gf('django.db.models.fields.BigIntegerField')())
        db.alter_column(u'servers_server', 'number_cores', self.gf('django.db.models.fields.PositiveSmallIntegerField')())
        db.alter_column(u'servers_server', 'ram', self.gf('django.db.models.fields.BigIntegerField')())

    def backwards(self, orm):

        db.alter_column(u'servers_server', 'bandwidth', self.gf('django.db.models.fields.IntegerField')())
        db.alter_column(u'servers_server', 'burst', self.gf('django.db.models.fields.IntegerField')())
        db.alter_column(u'servers_server', 'hdd_space', self.gf('django.db.models.fields.IntegerField')())
        db.alter_column(u'servers_server', 'number_cores', self.gf('django.db.models.fields.IntegerField')())
        db.alter_column(u'servers_server', 'ram', self.gf('django.db.models.fields.IntegerField')())

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
        u'servers.responderapi': {
            'Meta': {'object_name': 'ResponderAPI'},
            'api_key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'api_port': ('django.db.models.fields.IntegerField', [], {'max_length': '8'}),
            'api_url': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'server': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['servers.Server']", 'unique': 'True'})
        },
        u'servers.server': {
            'Meta': {'object_name': 'Server'},
            'bandwidth': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'billing_type': ('django.db.models.fields.CharField', [], {'default': "'m'", 'max_length': '1'}),
            'burst': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            'check_status': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '2'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'hdd_space': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'number_cores': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'purchased_at': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'purposes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['servers.Purpose']", 'null': 'True', 'blank': 'True'}),
            'ram': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
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
        },
        u'servers.solusapi': {
            'Meta': {'object_name': 'SolusAPI'},
            'api_hash': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'api_key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'api_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'server': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['servers.Server']", 'unique': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['servers']
