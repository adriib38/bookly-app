# Generated by Django 4.1.7 on 2023-05-22 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0037_alter_notification_notification_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='pic',
            field=models.ImageField(blank=True, upload_to='myapp/static/imgs/profiles'),
        ),
    ]