# Generated by Django 4.1.7 on 2023-04-24 15:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0015_listbook'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listbook',
            name='type_list',
            field=models.CharField(choices=[('leidos', 'Leidos'), ('leyendo', 'Leyendo'), ('por_leer', 'Por leer')], max_length=10),
        ),
        migrations.CreateModel(
            name='ListBookBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_id', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('list_book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.listbook')),
            ],
        ),
    ]
