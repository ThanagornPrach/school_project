from django.db import models
from django.contrib.auth.models import User

class Grade(models.Model):
    grade = models.CharField(max_length=1)
    def __str__(self):
        return str(self.grade)

class School(models.Model):
    school = models.CharField(max_length=20)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return str(self.school)

class Student(models.Model):
    student = models.CharField(max_length=20)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, null=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.student)

class Parent(models.Model):
    parent = models.CharField(max_length=20)
    children = models.ManyToManyField(Student)
    def __str__(self):
        return str(self.parent)
