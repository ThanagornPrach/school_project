# Generated by Django 3.2.4 on 2021-07-13 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolapp', '0024_alter_grade_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grade',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]