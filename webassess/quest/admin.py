from django.contrib import admin
from quest.models import (
            Test,
            Tag,
            Question,
            AnswerOption,
            AnswerSave,
            TestSave)
"""
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 3


class TestAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['creator']}),
        ('Date information', {'fields': ['postdate', 'enddate'],
                              'classes': ['collapse']}),
    ]
    inlines = [QuestionInline]
"""
admin.site.register(Test) #, TestAdmin)
admin.site.register(Question)
admin.site.register(Tag)
admin.site.register(AnswerOption)
admin.site.register(AnswerSave)
admin.site.register(TestSave)
