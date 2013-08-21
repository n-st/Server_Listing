# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Server.number_cores'
        db.add_column(u'servers_server', 'number_cores',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Adding field 'Server.bandwidth'
        db.add_column(u'servers_server', 'bandwidth',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Server.ram'
        db.add_column(u'servers_server', 'ram',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Server.burst'
        db.add_column(u'servers_server', 'burst',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Server.hdd_space'
        db.add_column(u'servers_server', 'hdd_space',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Server.virt_type'
        db.add_column(u'servers_server', 'virt_type',
                      self.gf('django.db.models.fields.CharField')(default='o', max_length=1),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Server.number_cores'
        db.delete_column(u'servers_server', 'number_cores')

        # Deleting field 'Server.bandwidth'
        db.delete_column(u'servers_server', 'bandwidth')

        # Deleting field 'Server.ram'
        db.delete_column(u'servers_server', 'ram')

        # Deleting field 'Server.burst'
        db.delete_column(u'servers_server', 'burst')

        # Deleting field 'Server.hdd_space'
        db.delete_column(u'servers_server', 'hdd_space')

        # Deleting field 'Server.virt_type'
        db.delete_column(u'servers_server', 'virt_type')


    models = {
        u'servers.extra_ip': {
            'Meta': {'object_name': 'Extra_IP'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['servers.Server']"})
        },
        u'servers.server': {
            'Meta': {'object_name': 'Server'},
            'bandwidth': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'billing_type': ('django.db.models.fields.CharField', [], {'default': "'m'", 'max_length': '1'}),
            'burst': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '2'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'hdd_space': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'number_cores': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'purchased_at': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'ram': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'virt_type': ('django.db.models.fields.CharField', [], {'default': "'o'", 'max_length': '1'})
        }
    }

    complete_apps = ['servers']