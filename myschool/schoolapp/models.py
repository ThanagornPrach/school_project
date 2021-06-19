from django.db import models

class Level(models.Model):
    level = models.CharField(max_length=1)
    def __str__(self):
        return str(self.level)

class School(models.Model):
    school = models.CharField(max_length=20)
    def __str__(self):
        return str(self.school)

class Student(models.Model):
    student = models.CharField(max_length=20)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.student)

class Parent(models.Model):
    parent = models.CharField(max_length=20)
    children = models.ManyToManyField(Student)
    def __str__(self):
        return str(self.parent)
