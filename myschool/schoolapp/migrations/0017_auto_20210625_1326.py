# Generated by Django 3.2.4 on 2021-06-25 06:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schoolapp', '0016_auto_20210624_1649'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='school',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='student',
            name='user',
        ),
    ]
