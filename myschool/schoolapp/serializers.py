from django.db.models import fields
from rest_framework import serializers
from .models import *

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['school']

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['grade']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['student']

class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = ['parent']
