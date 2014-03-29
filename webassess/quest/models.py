from django.db import models

from users import Teacher

class Tag(models.Model):
    name = models.CharField(max_length=20)

class Question(models.Model):
    qtype = models.IntegerField(default=0)

class Test(models.Model):
    num = models.IntegerField(default=0)
    postdate = models.DataTimeField('date published')
    creator = models.ForeignKey(Teacher)
    enddate = models.DataTimeField('date of closing')
    questions = models.ManyToManyField(Question)

# Create your models here.
