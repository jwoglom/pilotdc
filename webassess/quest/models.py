from django.db import models

from users.models import Teacher
import datetime

class Tag(models.Model):
    name = models.CharField(max_length=20)

class Question(models.Model):
    qtype = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag)
    header = models.CharField(default="", max_length=2000)
    choices = models.CharField(default="", max_length=2000)
    answer = models.CharField(default="", max_length=1000)
class Test(models.Model):
    num = models.IntegerField(default=0)
    postdate = models.DateTimeField('date published',
            default=datetime.datetime.now,
            blank=True,
            )
    creator = models.ForeignKey(Teacher, null=True)
    enddate = models.DateTimeField('date of closing',
            default=lambda: datetime.datetime.now() + datetime.timedelta(days=9999),
            blank=True
            )
    questions = models.ManyToManyField(Question)

# Create your models here.
