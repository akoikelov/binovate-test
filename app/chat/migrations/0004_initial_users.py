# Generated by Django 2.2.10 on 2021-06-03 19:30
from django.contrib.auth.hashers import make_password
from django.db import migrations


def create_users(apps, schema_editor):
    User = apps.get_model('auth', 'User')

    User.objects.create(username='admin1234', password=make_password('admin'), is_superuser=True, is_staff=True)

    User.objects.create(username='test1', password=make_password('test1'))
    User.objects.create(username='test2', password=make_password('test2'))


def delete_users(apps, schema_editor):
    User = apps.get_model('auth', 'User')

    User.objects.filter(username__in=['admin1234', 'test1', 'test2']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_auto_20210603_1757'),
    ]

    operations = [
        migrations.RunPython(create_users, delete_users)
    ]
