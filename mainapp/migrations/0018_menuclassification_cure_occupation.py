# Generated by Django 2.1 on 2018-09-19 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0017_remove_menuclassification_cure_occupation'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuclassification',
            name='cure_occupation',
            field=models.ManyToManyField(blank=True, null=True, to='mainapp.Occupation'),
        ),
    ]
