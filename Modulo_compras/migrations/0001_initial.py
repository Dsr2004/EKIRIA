# Generated by Django 3.2.9 on 2022-06-06 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id_proveedor', models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name='id_proveedor')),
                ('nombre', models.CharField(max_length=20, unique=True)),
                ('telefono', models.CharField(blank=True, max_length=10, null=True)),
                ('celular', models.CharField(max_length=10, unique=True)),
                ('descripcion', models.TextField(blank=True, max_length=200, null=True)),
                ('estado', models.BooleanField(default=True, verbose_name='estado')),
            ],
            options={
                'verbose_name': 'Proveedor',
                'verbose_name_plural': 'Proveedores',
                'db_table': 'Proveedor',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Tipo_producto',
            fields=[
                ('id_tipo_producto', models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name='id_tipo_producto')),
                ('nombre', models.CharField(max_length=20, unique=True)),
                ('estado', models.BooleanField(default=True, verbose_name='estado')),
            ],
            options={
                'verbose_name': 'Tipo_producto',
                'verbose_name_plural': 'Tipo_productos',
                'db_table': 'Tipo_producto',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id_producto', models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name='id_producto')),
                ('nombre', models.CharField(max_length=20, unique=True, verbose_name='nombre del producto')),
                ('precio', models.IntegerField(verbose_name='precio')),
                ('cantidad', models.IntegerField(verbose_name='cantidad')),
                ('estado', models.BooleanField(default=True, verbose_name='estado')),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Modulo_compras.proveedor')),
                ('tipo_producto', models.ForeignKey(blank=True, db_column='tipo_producto_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='Modulo_compras.tipo_producto', verbose_name='Tipo de producto')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
                'db_table': 'Producto',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id_compras', models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name='id_compra')),
                ('cantidad', models.IntegerField(verbose_name='cantidad')),
                ('total', models.FloatField()),
                ('estado', models.BooleanField(default=True, verbose_name='estado')),
                ('fecha_creacion', models.DateField(auto_now_add=True, verbose_name='fecha_creacion')),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualizacion')),
                ('producto', models.ManyToManyField(to='Modulo_compras.Producto')),
            ],
            options={
                'verbose_name': 'Compra',
                'verbose_name_plural': 'Compras',
                'db_table': 'Compra',
                'ordering': ['id_compras'],
            },
        ),
    ]
