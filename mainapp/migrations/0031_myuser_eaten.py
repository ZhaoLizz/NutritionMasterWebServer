# Generated by Django 2.1.1 on 2018-09-30 13:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0030_myuser_bmi'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='eaten',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.Element'),
        ),
    ]