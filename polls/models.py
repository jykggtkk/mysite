from __future__ import unicode_literals
import datetime
from django.db import models
from django.utils import timezone

# Create your models here.

class Question(models.Model):
    question_text=models.CharField(max_length=200)
    pub_date=models.DateTimeField('date published')
    #python3 =  __str__
    def __unicode__(self):
           return self.question_text
    #user define
    def was_published_recently(self):
           now=timezone.now()
           return  now - datetime.timedelta(days=4)<=self.pub_date <=now
           was_published_recently.admin_order_field='pub_date'
           was_published_recently.boolean=True
           was_published_recently.short_desciption="Published recently"

class Choice(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    choice_text=models.CharField(max_length=200)
    votes=models.IntegerField(default=0)
    #python3 =  __str_
    def __unicode__(self):
           return self.choice_text
