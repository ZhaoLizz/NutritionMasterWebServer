# Generated by Django 2.1 on 2018-09-20 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0019_auto_20180920_1143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='physique',
            name='exercise_method',
        ),
        migrations.RemoveField(
            model_name='physique',
            name='physical_feature',
        ),
    ]
