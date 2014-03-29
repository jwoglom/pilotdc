from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=20)

class Question(models.Model):
    qtype = models.IntegerField(default=0)

class Test(models.Model):
    num = models.IntegerField(default=0)
    questions = models.ManyToManyField(Question)

# Create your models here.
