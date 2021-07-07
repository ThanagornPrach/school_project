from django.contrib import admin
from .models import *

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['user','name', 'description']

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
	list_display = ['school','name', 'description', 'pk']



@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
	list_display = ['director','first_name', 'last_name', 'pk']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
	list_display = ['pk','first_name', 'last_name']

