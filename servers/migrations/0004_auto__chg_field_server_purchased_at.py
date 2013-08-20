# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Server.purchased_at'
        db.alter_column(u'servers_server', 'purchased_at', self.gf('django.db.models.fields.DateField')())

    def backwards(self, orm):

        # Changing field 'Server.purchased_at'
        db.alter_column(u'servers_server', 'purchased_at', self.gf('django.db.models.fields.DateTimeField')())

    models = {
        u'servers.extra_ip': {
            'Meta': {'object_name': 'Extra_IP'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['servers.Server']"})
        },
        u'servers.server': {
            'Meta': {'object_name': 'Server'},
            'billing_type': ('django.db.models.fields.CharField', [], {'default': "'m'", 'max_length': '1'}),
            'cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '2'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'purchased_at': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['servers']