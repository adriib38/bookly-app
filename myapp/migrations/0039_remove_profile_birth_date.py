# Generated by Django 4.1.7 on 2023-05-22 22:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0038_profile_pic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='birth_date',
        ),
    ]
