# Generated by Django 2.1 on 2018-09-19 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0013_uploadfile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='occupation',
            name='id',
        ),
        migrations.AlterField(
            model_name='occupation',
            name='occupation_name',
            field=models.CharField(max_length=16, primary_key=True, serialize=False, unique=True),
        ),
    ]
