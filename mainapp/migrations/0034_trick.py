# Generated by Django 2.1.1 on 2018-10-01 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0033_auto_20181001_2104'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trick',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('content', models.TextField()),
            ],
        ),
    ]