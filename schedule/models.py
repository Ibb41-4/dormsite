from django.db import models

# Create your models here.

class Week(models.Model):
    startdate = models.DateField()

class Task(models.Model):
    name = models.CharField(max_length=200)    

class Shift(models.Model):
    week = models.ForeignKey(Week)
    user = models.ForeignKey('User')
    task = models.ForeignKey(Task)
