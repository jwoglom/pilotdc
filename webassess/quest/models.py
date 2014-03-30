from django.db import models

from users.models import Teacher
import datetime

class Tag(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name

    def __unicode__(self):
        return "{0}".format(self.name)

class AnswerOption(models.Model):
    text = models.CharField(default="", max_length=10000)

    def __unicode__(self):
        return "{0}".format(self.text)

class Question(models.Model):
    qtype = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, related_name='tags')
    header = models.CharField(default="", max_length=10000)
    #choices = models.CharField(default="", max_length=10000)
    choices = models.ManyToManyField(AnswerOption, related_name='answer_choices')
    #answer = models.CharField(default="", max_length=10000)
    answer = models.ForeignKey(AnswerOption, null=True, related_name='answer_correct')
    def __unicode__(self):
        return "{0} ({1}): {2}: {3}".format(self.header, self.qtype, self.choices, self.answer)

class Test(models.Model):
#    num = models.IntegerField(default=0)
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
    def __str__(self):
        return "Test #" + str(self.id)

# Create your models here.
