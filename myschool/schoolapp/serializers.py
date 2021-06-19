from rest_framework import serializers
from .models import *

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['school']

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['level']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['student']

class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = ['parent']