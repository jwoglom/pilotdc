from django.db import models

from users.models import Teacher

class Tag(models.Model):
    name = models.CharField(max_length=20)

class Question(models.Model):
    qtype = models.IntegerField(default=0)

class Test(models.Model):
    num = models.IntegerField(default=0)
    postdate = models.DateTimeField('date published')
    creator = models.ForeignKey(Teacher)
    enddate = models.DateTimeField('date of closing')
    questions = models.ManyToManyField(Question)

# Create your models here.
