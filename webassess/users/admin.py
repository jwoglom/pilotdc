from django.contrib import admin

from users.models import (
            School,
            Teacher,
            Student,
            )

admin.site.register(Teacher)
admin.site.register(School)
admin.site.register(Student)
# Register your models here.
