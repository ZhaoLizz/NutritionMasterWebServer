# Generated by Django 2.1 on 2018-09-07 07:12

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='FoodMaterial',
            fields=[
                ('material_name', models.CharField(max_length=64, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('name', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('calorie', models.IntegerField()),
                ('minutes', models.IntegerField()),
                ('flavor', models.CharField(max_length=64)),
                ('technology', models.CharField(max_length=16)),
                ('image_url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='MenuClassification',
            fields=[
                ('classification', models.CharField(max_length=16, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Occupation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('occupation_name', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='PhysicalProperty',
            fields=[
                ('property_name', models.CharField(max_length=64, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Physique',
            fields=[
                ('physical_name', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('physical_feature', models.TextField()),
                ('exercise_method', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='menu',
            name='physical_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Physique'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='occupation_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.Occupation'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='physical_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.Physique'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
