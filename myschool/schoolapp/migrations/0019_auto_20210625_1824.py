# Generated by Django 3.2.4 on 2021-06-25 11:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schoolapp', '0018_school_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grade',
            name='level',
        ),
        migrations.RemoveField(
            model_name='school',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='school',
            name='school_name',
        ),
        migrations.RemoveField(
            model_name='school',
            name='student',
        ),
        migrations.RemoveField(
            model_name='student',
            name='student_name',
        ),
        migrations.AddField(
            model_name='grade',
            name='description',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='grade',
            name='name',
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='grade',
            name='school',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='schoolapp.school'),
        ),
        migrations.AddField(
            model_name='school',
            name='description',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='school',
            name='name',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='first_name',
            field=models.CharField(max_length=125, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='last_name',
            field=models.CharField(max_length=125, null=True),
        ),
        migrations.DeleteModel(
            name='Parent',
        ),
    ]
