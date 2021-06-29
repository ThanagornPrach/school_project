from django.contrib import admin
from .models import *

admin.site.register(School)
admin.site.register(Grade)


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
	list_display = ['director','first_name', 'last_name']

admin.site.register(Student)

