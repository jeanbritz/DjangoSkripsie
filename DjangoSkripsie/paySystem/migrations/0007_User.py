# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'User'
        db.create_table(u'paySystem_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30, db_index=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('contactnumber', self.gf('django.db.models.fields.CharField')(default='', max_length=12, blank=True)),
            ('acct_balance', self.gf('django.db.models.fields.IntegerField')(default=50)),
            ('acct_available', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=254)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='locations', null=True, to=orm['paySystem.Locations'])),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_consumer', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_vendor', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'paySystem', ['User'])

        # Adding M2M table for field groups on 'User'
        m2m_table_name = db.shorten_name(u'paySystem_user_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm[u'paySystem.user'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['user_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'User'
        m2m_table_name = db.shorten_name(u'paySystem_user_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm[u'paySystem.user'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['user_id', 'permission_id'])

        # Adding model 'UserProfile'
        db.create_table(u'paySystem_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['paySystem.User'], unique=True)),
            ('contactnumber', self.gf('django.db.models.fields.CharField')(default='', max_length=12, blank=True)),
            ('acct_balance', self.gf('django.db.models.fields.IntegerField')(default=50)),
            ('acct_available', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'paySystem', ['UserProfile'])

        # Adding model 'NFCDevices'
        db.create_table(u'paySystem_nfcdevices', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='nfcdevices', to=orm['paySystem.User'])),
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=13, blank=True)),
        ))
        db.send_create_signal(u'paySystem', ['NFCDevices'])

        # Adding model 'Claims'
        db.create_table(u'paySystem_claims', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='claims', to=orm['paySystem.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=8, blank=True)),
            ('expiry_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('claimed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('amount', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'paySystem', ['Claims'])

        # Adding model 'Invoices'
        db.create_table(u'paySystem_invoices', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='invoices', to=orm['paySystem.User'])),
            ('amount_payable', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('issued_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'paySystem', ['Invoices'])

        # Adding model 'Transactions'
        db.create_table(u'paySystem_transactions', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transactions', to=orm['paySystem.User'])),
            ('invoice', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transactions', to=orm['paySystem.Invoices'])),
            ('processed_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('amount', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('debit_credit', self.gf('django.db.models.fields.CharField')(max_length=6)),
        ))
        db.send_create_signal(u'paySystem', ['Transactions'])

        # Adding model 'Locations'
        db.create_table(u'paySystem_locations', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('mcc', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('mnc', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('network', self.gf('django.db.models.fields.CharField')(default='GSM', max_length=5)),
            ('lac', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('cell_id', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'paySystem', ['Locations'])


    def backwards(self, orm):
        # Deleting model 'User'
        db.delete_table(u'paySystem_user')

        # Removing M2M table for field groups on 'User'
        db.delete_table(db.shorten_name(u'paySystem_user_groups'))

        # Removing M2M table for field user_permissions on 'User'
        db.delete_table(db.shorten_name(u'paySystem_user_user_permissions'))

        # Deleting model 'UserProfile'
        db.delete_table(u'paySystem_userprofile')

        # Deleting model 'NFCDevices'
        db.delete_table(u'paySystem_nfcdevices')

        # Deleting model 'Claims'
        db.delete_table(u'paySystem_claims')

        # Deleting model 'Invoices'
        db.delete_table(u'paySystem_invoices')

        # Deleting model 'Transactions'
        db.delete_table(u'paySystem_transactions')

        # Deleting model 'Locations'
        db.delete_table(u'paySystem_locations')


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