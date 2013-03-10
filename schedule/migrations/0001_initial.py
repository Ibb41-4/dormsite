# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Week'
        db.create_table(u'schedule_week', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('year', self.gf('django.db.models.fields.PositiveIntegerField')(default=2013)),
        ))
        db.send_create_signal(u'schedule', ['Week'])

        # Adding model 'Task'
        db.create_table(u'schedule_task', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'schedule', ['Task'])

        # Adding model 'Shift'
        db.create_table(u'schedule_shift', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('week', self.gf('django.db.models.fields.related.ForeignKey')(related_name='shifts', to=orm['schedule.Week'])),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(related_name='shifts', to=orm['residents.Room'])),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(related_name='shifts', to=orm['schedule.Task'])),
            ('done', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'schedule', ['Shift'])

        # Adding unique constraint on 'Shift', fields ['week', 'task']
        db.create_unique(u'schedule_shift', ['week_id', 'task_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Shift', fields ['week', 'task']
        db.delete_unique(u'schedule_shift', ['week_id', 'task_id'])

        # Deleting model 'Week'
        db.delete_table(u'schedule_week')

        # Deleting model 'Task'
        db.delete_table(u'schedule_task')

        # Deleting model 'Shift'
        db.delete_table(u'schedule_shift')


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
        u'residents.room': {
            'Meta': {'ordering': "['number']", 'object_name': 'Room'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True'}),
            'tasks': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'rooms'", 'symmetrical': 'False', 'to': u"orm['schedule.Task']"}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'rooms'", 'symmetrical': 'False', 'through': u"orm['residents.RoomAssignment']", 'to': u"orm['residents.User']"})
        },
        u'residents.roomassignment': {
            'Meta': {'ordering': "['start_date']", 'object_name': 'RoomAssignment'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'roomassignments'", 'to': u"orm['residents.Room']"}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'roomassignments'", 'to': u"orm['residents.User']"})
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
        },
        u'schedule.shift': {
            'Meta': {'unique_together': "(('week', 'task'),)", 'object_name': 'Shift'},
            'done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'shifts'", 'to': u"orm['residents.Room']"}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'shifts'", 'to': u"orm['schedule.Task']"}),
            'week': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'shifts'", 'to': u"orm['schedule.Week']"})
        },
        u'schedule.task': {
            'Meta': {'object_name': 'Task'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'schedule.week': {
            'Meta': {'object_name': 'Week'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {'default': '2013'})
        }
    }

    complete_apps = ['schedule']