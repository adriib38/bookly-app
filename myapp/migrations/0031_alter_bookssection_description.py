# Generated by Django 4.1.7 on 2023-05-13 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0030_alter_bookssection_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookssection',
            name='description',
            field=models.TextField(blank=True, default='', max_length=500),
        ),
    ]