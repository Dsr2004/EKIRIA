# Generated by Django 3.2.9 on 2022-03-27 21:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Usuarios', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vistasdiarias',
            name='fecha',
        ),
    ]
