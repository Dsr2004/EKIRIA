# Generated by Django 3.2.9 on 2022-06-13 11:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Ventas', '0002_alter_catalogo_servicio_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalogo',
            name='servicio_id',
            field=models.ForeignKey(blank=True, db_column='servicio_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='Ventas.servicio', verbose_name='Servicio'),
        ),
    ]
