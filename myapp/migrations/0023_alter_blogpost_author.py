# Generated by Django 4.1.7 on 2023-04-29 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0022_alter_groupreaders_image_blogpost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='author',
            field=models.TextField(max_length=100),
        ),
    ]
