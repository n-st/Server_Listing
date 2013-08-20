# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Extra_IP'
        db.create_table(u'servers_extra_ip', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('server', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['servers.Server'])),
            ('ip', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
        ))
        db.send_create_signal(u'servers', ['Extra_IP'])

        # Adding field 'Server.main_ip'
        db.add_column(u'servers_server', 'main_ip',
                      self.gf('django.db.models.fields.GenericIPAddressField')(default=u'0.0.0.0', max_length=39),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Extra_IP'
        db.delete_table(u'servers_extra_ip')

        # Deleting field 'Server.main_ip'
        db.delete_column(u'servers_server', 'main_ip')


    models = {
        u'servers.extra_ip': {
            'Meta': {'object_name': 'Extra_IP'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['servers.Server']"})
        },
        u'servers.server': {
            'Meta': {'object_name': 'Server'},
            'cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '2'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['servers']