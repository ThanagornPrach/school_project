# Generated by Django 3.2.4 on 2021-06-25 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolapp', '0017_auto_20210625_1326'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='parent',
            field=models.ManyToManyField(to='schoolapp.Parent'),
        ),
    ]
