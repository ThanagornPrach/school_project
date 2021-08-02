from django.db import models
from django.contrib.auth.models import User




########################## v1
# class Grade(models.Model):
#     level = models.CharField(max_length=1)
#     def __str__(self):
#         return str(self.level)

# class School(models.Model):
#     school_name = models.CharField(max_length=20)
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
#     def __str__(self):
#         return str(self.school_name)

# class Student(models.Model):
#     student_name = models.CharField(max_length=20)
#     grade = models.ForeignKey(Grade, on_delete=models.CASCADE, null=True)
#     school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

#     def __str__(self):
#         return str(self.student_name)

# class Parent(models.Model):
#     parent_name = models.CharField(max_length=20)
#     children = models.ManyToManyField(Student)
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
#     def __str__(self):
#         return str(self.parent_name)

############################ v2
# class Grade(models.Model):
#     level = models.CharField(max_length=1)
#     def __str__(self):
#         return str(self.level)

# class Student(models.Model):
#     student_name = models.CharField(max_length=20)
#     grade = models.ForeignKey(Grade, on_delete=models.CASCADE, null=True)
#     # school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)
#     # user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

#     def __str__(self):
#         return str(self.student_name)

# class Parent(models.Model):
#     parent_name = models.CharField(max_length=20)
#     children = models.ManyToManyField(Student)
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
#     def __str__(self):
#         return str(self.parent_name)
        
# class School(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
#     school_name = models.CharField(max_length=20)
#     student = models.ManyToManyField(Student)
#     parent = models.ManyToManyField(Parent)
#     def __str__(self):
#         return str(self.school_name)


########################## v3
class School(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    name = models.CharField(max_length=20, null=True)
    description = models.CharField(max_length=255, null=True)
    def __str__(self):
        return str(self.name)


class Grade(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)

    name = models.CharField(max_length=200, null=True) # None
    description = models.CharField(max_length=255, null=True)
    def __str__(self):
        return str(self.name)

class Student(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, null=True)

    first_name = models.CharField(max_length=125, null=True)
    last_name = models.CharField(max_length=125, null=True)
    nick_name = models.CharField(max_length=125, null=True)
    def __str__(self):
        return '%s - %s - %s ' % (self.first_name, self.last_name, self.nick_name)

class Parent(models.Model):
    director = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    children = models.ManyToManyField(Student)

    first_name = models.CharField(max_length=125, null=True)
    last_name = models.CharField(max_length=125, null=True)
    def __str__(self):
        return '%s - %s' % (self.first_name, self.last_name)




    



