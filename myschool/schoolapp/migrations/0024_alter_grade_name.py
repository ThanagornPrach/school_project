# Generated by Django 3.2.4 on 2021-07-09 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolapp', '0023_alter_grade_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grade',
            name='name',
            field=models.CharField(max_length=20, null=True),
        ),
    ]