# Generated by Django 4.1.7 on 2023-05-25 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0040_alter_profile_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(max_length=290),
        ),
    ]