# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Balance'
        db.create_table(u'balance_balance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='added_balance', to=orm['residents.User'])),
            ('modified_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='changed_balance', to=orm['residents.User'])),
            ('preview', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'balance', ['Balance'])

        # Adding model 'BalanceRow'
        db.create_table(u'balance_balancerow', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['residents.User'])),
            ('balance', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rows', to=orm['balance.Balance'])),
            ('last_balance', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=2)),
            ('payed', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=2)),
            ('expenses', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=2)),
            ('monthly_fee', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=2)),
            ('dinners', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=2)),
            ('drinks', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=2)),
            ('total', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=2)),
        ))
        db.send_create_signal(u'balance', ['BalanceRow'])

        # Adding model 'Bill'
        db.create_table(u'balance_bill', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='added_bill', to=orm['residents.User'])),
            ('modified_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='changed_bill', to=orm['residents.User'])),
            ('payer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='payed_bills', to=orm['residents.User'])),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'balance', ['Bill'])

        # Adding model 'Expense'
        db.create_table(u'balance_expense', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='added_expense', to=orm['residents.User'])),
            ('modified_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='changed_expense', to=orm['residents.User'])),
            ('payer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='payed_expenses', to=orm['residents.User'])),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'balance', ['Expense'])

        # Adding model 'Drink'
        db.create_table(u'balance_drink', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='added_drink', to=orm['residents.User'])),
            ('modified_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='changed_drink', to=orm['residents.User'])),
            ('payer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='payed_drinks', to=orm['residents.User'])),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('number', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'balance', ['Drink'])

        # Adding model 'Dinner'
        db.create_table(u'balance_dinner', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='added_dinner', to=orm['residents.User'])),
            ('modified_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='changed_dinner', to=orm['residents.User'])),
            ('payer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='payed_dinners', to=orm['residents.User'])),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
        ))
        db.send_create_signal(u'balance', ['Dinner'])

        # Adding model 'Eater'
        db.create_table(u'balance_eater', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dinner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['balance.Dinner'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['residents.User'])),
            ('extra', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'balance', ['Eater'])


    def backwards(self, orm):
        # Deleting model 'Balance'
        db.delete_table(u'balance_balance')

        # Deleting model 'BalanceRow'
        db.delete_table(u'balance_balancerow')

        # Deleting model 'Bill'
        db.delete_table(u'balance_bill')

        # Deleting model 'Expense'
        db.delete_table(u'balance_expense')

        # Deleting model 'Drink'
        db.delete_table(u'balance_drink')

        # Deleting model 'Dinner'
        db.delete_table(u'balance_dinner')

        # Deleting model 'Eater'
        db.delete_table(u'balance_eater')


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
        u'balance.balance': {
            'Meta': {'object_name': 'Balance'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'added_balance'", 'to': u"orm['residents.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'changed_balance'", 'to': u"orm['residents.User']"}),
            'preview': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'balance.balancerow': {
            'Meta': {'object_name': 'BalanceRow'},
            'balance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rows'", 'to': u"orm['balance.Balance']"}),
            'dinners': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'drinks': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'expenses': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_balance': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'monthly_fee': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'payed': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'total': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['residents.User']"})
        },
        u'balance.bill': {
            'Meta': {'object_name': 'Bill'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'added_bill'", 'to': u"orm['residents.User']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'changed_bill'", 'to': u"orm['residents.User']"}),
            'payer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payed_bills'", 'to': u"orm['residents.User']"}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'})
        },
        u'balance.dinner': {
            'Meta': {'object_name': 'Dinner'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'added_dinner'", 'to': u"orm['residents.User']"}),
            'eaters': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'dinners'", 'symmetrical': 'False', 'through': u"orm['balance.Eater']", 'to': u"orm['residents.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'changed_dinner'", 'to': u"orm['residents.User']"}),
            'payer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payed_dinners'", 'to': u"orm['residents.User']"}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'})
        },
        u'balance.drink': {
            'Meta': {'object_name': 'Drink'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'added_drink'", 'to': u"orm['residents.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'changed_drink'", 'to': u"orm['residents.User']"}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'payer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payed_drinks'", 'to': u"orm['residents.User']"}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'})
        },
        u'balance.eater': {
            'Meta': {'object_name': 'Eater'},
            'dinner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['balance.Dinner']"}),
            'extra': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['residents.User']"})
        },
        u'balance.expense': {
            'Meta': {'object_name': 'Expense'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'added_expense'", 'to': u"orm['residents.User']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'changed_expense'", 'to': u"orm['residents.User']"}),
            'payer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payed_expenses'", 'to': u"orm['residents.User']"}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'residents.user': {
            'Meta': {'ordering': "['first_name', 'last_name']", 'object_name': 'User'},
            'birthdate': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'emergency_phonenumber': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phonenumber': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['balance']