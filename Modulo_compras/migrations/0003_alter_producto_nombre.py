# Generated by Django 3.2.9 on 2022-06-16 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Modulo_compras', '0002_alter_proveedor_telefono'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='nombre',
            field=models.CharField(max_length=50, verbose_name='nombre del producto'),
        ),
    ]