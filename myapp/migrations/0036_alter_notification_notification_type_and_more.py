# Generated by Django 4.1.7 on 2023-05-17 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0035_alter_notification_notification_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.IntegerField(blank=True, choices=[(1, 'Mencion'), (2, 'Comentario'), (3, 'Follow')], null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='to_user',
            field=models.CharField(max_length=150, null=True),
        ),
    ]