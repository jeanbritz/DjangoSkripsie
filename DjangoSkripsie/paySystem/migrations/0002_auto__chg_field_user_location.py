# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'User.location'
        db.alter_column(u'paySystem_user', 'location_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['paySystem.Locations']))

    def backwards(self, orm):

        # Changing field 'User.location'
        db.alter_column(u'paySystem_user', 'location_id', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['paySystem.Locations']))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'paySystem.claims': {
            'Meta': {'ordering': "('expiry_date',)", 'object_name': 'Claims'},
            'amount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'claimed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'expiry_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'claims'", 'to': u"orm['paySystem.User']"})
        },
        u'paySystem.invoices': {
            'Meta': {'ordering': "('issued_date',)", 'object_name': 'Invoices'},
            'amount_payable': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issued_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invoices'", 'to': u"orm['paySystem.User']"})
        },
        u'paySystem.locations': {
            'Meta': {'object_name': 'Locations'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'cell_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lac': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'mcc': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'mnc': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'network': ('django.db.models.fields.CharField', [], {'default': "'GSM'", 'max_length': '5'})
        },
        u'paySystem.nfcdevices': {
            'Meta': {'object_name': 'NFCDevices'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '13', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nfcdevices'", 'to': u"orm['paySystem.User']"})
        },
        u'paySystem.transactions': {
            'Meta': {'ordering': "('processed_date',)", 'object_name': 'Transactions'},
            'amount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'debit_credit': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transactions'", 'to': u"orm['paySystem.Invoices']"}),
            'processed_date': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transactions'", 'to': u"orm['paySystem.User']"})
        },
        u'paySystem.user': {
            'Meta': {'object_name': 'User'},
            'acct_available': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'acct_balance': ('django.db.models.fields.IntegerField', [], {'default': '50'}),
            'contactnumber': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '12', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '254'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_consumer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_vendor': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'locations'", 'null': 'True', 'to': u"orm['paySystem.Locations']"}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30', 'db_index': 'True'})
        },
        u'paySystem.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'acct_available': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'acct_balance': ('django.db.models.fields.IntegerField', [], {'default': '50'}),
            'contactnumber': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '12', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['paySystem.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['paySystem']