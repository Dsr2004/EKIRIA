# Generated by Django 3.2.9 on 2022-06-06 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Modulo_compras', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistorialCompra',
            fields=[
                ('id_HC', models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name='id_HC')),
                ('precio', models.FloatField()),
                ('cantidad', models.IntegerField()),
            ],
        ),
    ]