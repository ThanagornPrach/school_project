from django.contrib import admin
from .models import *

admin.site.register(School)

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
	list_display = ['school','name', 'description', 'pk']



@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
	list_display = ['director','first_name', 'last_name']

admin.site.register(Student)

