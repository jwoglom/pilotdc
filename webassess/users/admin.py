from django.contrib import admin

from users.models import (
            Teacher,
            Student,
            )

admin.site.register(Teacher)
admin.site.register(Student)
# Register your models here.
