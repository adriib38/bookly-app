# Generated by Django 4.1.7 on 2023-04-30 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0024_rename_writter_profile_writer_solicitudwriter'),
    ]

    operations = [
        migrations.AddField(
            model_name='resenya',
            name='stars',
            field=models.IntegerField(default=0),
        ),
    ]