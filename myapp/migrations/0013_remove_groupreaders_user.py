# Generated by Django 4.1.7 on 2023-04-22 23:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_membergroup_groupreaders_members'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupreaders',
            name='user',
        ),
    ]