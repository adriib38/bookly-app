# Generated by Django 4.1.7 on 2023-04-01 16:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_rename_user_post_author_post_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='date',
            new_name='created_at',
        ),
    ]
