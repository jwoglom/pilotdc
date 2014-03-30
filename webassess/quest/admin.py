from django.contrib import admin
from quest.models import (
            Test,
            Tag,
            Question,
            AnswerOption)

admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Tag)
admin.site.register(AnswerOption)
