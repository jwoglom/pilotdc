from django.db import models
from tinymce.models import HTMLField
#from users.models import Teacher
import datetime

class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return unicode(self.name)

class AnswerOption(models.Model):
    text = HTMLField()

    def __unicode__(self):
        return unicode(self.text)

class Question(models.Model):
    qtype = models.CharField(default="mc", max_length=10)
    tags = models.ManyToManyField(Tag, related_name='tags')
    #header = models.CharField(default="", max_length=10000)
    header = HTMLField()
    choices = models.ManyToManyField(AnswerOption, related_name='answer_choices')
    answer = models.ForeignKey(AnswerOption, null=True, related_name='answer_correct')
    def __unicode__(self):
        return unicode("{0} ({1})".format(self.id, self.qtype))

class Test(models.Model):
    postdate = models.DateTimeField('date published',
                default=datetime.datetime.now,
                blank=True,
            )
    creator = models.ForeignKey('users.Teacher', null=True)
    enddate = models.DateTimeField('date of closing',
                default=lambda: datetime.datetime.now() + datetime.timedelta(days=9999),
                blank=True
            )
    questions = models.ManyToManyField(Question)

    def __unicode__(self):
        return unicode(self.id)

class AnswerSave(models.Model):
    question = models.ForeignKey(Question)
    choice = models.ForeignKey('AnswerOption', null=True, blank=True)
    correct = models.BooleanField(default=False)

class TestSave(models.Model):
    user = models.ForeignKey('users.Student', null=True)
    test = models.ForeignKey(Test)
    saves = models.ManyToManyField(AnswerSave)
    score = models.IntegerField(default=0)
    def __unicode__(self):
        return unicode("")
