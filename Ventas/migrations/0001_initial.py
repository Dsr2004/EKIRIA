# Generated by Django 3.2.9 on 2022-03-27 20:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id_pedido', models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name='Id del Pedido')),
                ('completado', models.BooleanField(default=False, null=True)),
                ('esPersonalizado', models.BooleanField(default=False, verbose_name='Es personalizado')),
                ('fecha_creacion', models.DateField(auto_now_add=True, verbose_name='Fecha de Creacion')),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualizacion')),
                ('estado', models.BooleanField(default=True, verbose_name='Estado')),
                ('cliente_id', models.ForeignKey(blank=True, db_column='cliente_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'pedido',
                'verbose_name_plural': 'pedidos',
                'db_table': 'pedidos',
            },
        ),
        migrations.CreateModel(
            name='Tipo_servicio',
            fields=[
                ('id_tipo_servicio', models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name='Id del Tipo de Servicio')),
                ('nombre', models.CharField(max_length=50, unique=True, verbose_name='Nombre')),
                ('fecha_creacion', models.DateField(auto_now_add=True, verbose_name='Fecha de Creacion')),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualizacion')),
                ('estado', models.BooleanField(default=True, verbose_name='Estado')),
            ],
            options={
                'verbose_name': 'tipo de servicio',
                'verbose_name_plural': 'tipo_servicios',
                'db_table': 'tipo_servicios',
            },
        ),
        migrations.CreateModel(
            name='Servicio_Personalizado',
            fields=[
                ('id_servicio_personalizado', models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name='Id del Servicio Personalizado')),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='Descripcion')),
                ('img_servicio', models.ImageField(upload_to='Ventas/servicios_personalizados', verbose_name='Imagen del Servicio')),
                ('precio', models.IntegerField(blank=True, null=True, verbose_name='Precio')),
                ('duracion', models.PositiveIntegerField(default=0)),
                ('fecha_creacion', models.DateField(auto_now_add=True, verbose_name='Fecha de Creacion')),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualizacion')),
                ('estado', models.BooleanField(default=True, verbose_name='Estado')),
                ('tipo_servicio_id', models.ForeignKey(db_column='tipo_servicio_id', on_delete=django.db.models.deletion.CASCADE, to='Ventas.tipo_servicio', verbose_name='Tipo de Servicio')),
            ],
            options={
                'verbose_name': 'servicio personalizado',
                'verbose_name_plural': 'servicios_personalizados',
                'db_table': 'servicios_personalizados',
            },
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id_servicio', models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name='Id del Servicio')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
                ('nombre', models.CharField(max_length=40, unique=True, verbose_name='Nombre')),
                ('descripcion', models.TextField(verbose_name='Descripcion')),
                ('img_servicio', models.ImageField(upload_to='Ventas/servicios', verbose_name='Imagen del Servicio')),
                ('precio', models.IntegerField(verbose_name='Precio')),
                ('duracion', models.PositiveIntegerField(default=0)),
                ('fecha_creacion', models.DateField(auto_now_add=True, verbose_name='Fecha de Creacion')),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualizacion')),
                ('estado', models.BooleanField(default=True, verbose_name='Estado')),
                ('tipo_servicio_id', models.ForeignKey(blank=True, db_column='tipo_servicio_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='Ventas.tipo_servicio', verbose_name='Tipo de Servicio')),
            ],
            options={
                'verbose_name': 'servicio',
                'verbose_name_plural': 'servicios',
                'db_table': 'servicios',
            },
        ),
        migrations.CreateModel(
            name='PedidoItem',
            fields=[
                ('id_pedidoItem', models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name='Id del Item del  Pedido')),
                ('cantidad', models.IntegerField(blank=True, default=1, null=True, verbose_name='Cantidad')),
                ('fecha_creacion', models.DateField(auto_now_add=True, verbose_name='Fecha de Creacion')),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualizacion')),
                ('estado', models.BooleanField(default=True, verbose_name='Estado')),
                ('pedido_id', models.ForeignKey(db_column='pedido_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='Ventas.pedido', verbose_name='Id del Pedido')),
                ('servicio_id', models.ForeignKey(db_column='servicio_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='Ventas.servicio', verbose_name='Id del Servicio')),
                ('servicio_personalizado_id', models.ForeignKey(db_column='servicio_personalizado_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='Ventas.servicio_personalizado', verbose_name='Servicios Personalizados')),
            ],
            options={
                'verbose_name': 'pedidoItem',
                'verbose_name_plural': 'pedidoItems',
                'db_table': 'pedidoItems',
            },
        ),
        migrations.CreateModel(
            name='Pedido_Personalizado',
            fields=[
                ('id_pedido_personalizado', models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name='Id del Pedido Personalizado')),
                ('cantidad', models.IntegerField(blank=True, default=1, null=True, verbose_name='Cantidad')),
                ('fecha_creacion', models.DateField(auto_now_add=True, verbose_name='Fecha de Creacion')),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualizacion')),
                ('estado', models.BooleanField(default=True, verbose_name='Estado')),
                ('pedido_id', models.ForeignKey(db_column='pedido_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='Ventas.pedido', verbose_name='Id del Pedido')),
                ('servicio_id', models.ForeignKey(db_column='servicio_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='Ventas.servicio', verbose_name='Id del Servicio')),
                ('servicio_personalizado_id', models.ForeignKey(db_column='servicio_personalizado_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='Ventas.servicio_personalizado', verbose_name='Servicios Personalizados')),
            ],
            options={
                'verbose_name': 'pedido personalizado',
                'verbose_name_plural': 'pedidos_personalizados',
                'db_table': 'pedidos_personalizados',
            },
        ),
        migrations.CreateModel(
            name='Cita',
            fields=[
                ('id_cita', models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name='Id de la Cita')),
                ('diaCita', models.DateField(verbose_name='Dia de la cita')),
                ('horaInicioCita', models.TimeField(verbose_name='Fecha de Inicio de la Cita')),
                ('horaFinCita', models.TimeField(verbose_name='Fecha de Fin de la Cita')),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='Descripcion')),
                ('fecha_creacion', models.DateField(auto_now_add=True, verbose_name='Fecha de Creacion')),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualizacion')),
                ('estado', models.BooleanField(default=True, verbose_name='Estado')),
                ('cliente_id', models.ForeignKey(blank=True, db_column='cliente_id', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cliente_id', to=settings.AUTH_USER_MODEL)),
                ('empleado_id', models.ForeignKey(blank=True, db_column='empleado_id', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='empleado_id', to=settings.AUTH_USER_MODEL)),
                ('pedido_id', models.ForeignKey(db_column='pedido_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='Ventas.pedido', verbose_name='Id del Pedido')),
            ],
            options={
                'verbose_name': 'cita',
                'verbose_name_plural': 'citas',
                'db_table': 'citas',
            },
        ),
        migrations.CreateModel(
            name='Catalogo',
            fields=[
                ('id_catalogo', models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name='Id del Catalogo')),
                ('fecha_creacion', models.DateField(auto_now_add=True, verbose_name='Fecha de Creacion')),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True, verbose_name='Fecha de Actualizacion')),
                ('estado', models.BooleanField(default=True, verbose_name='Estado')),
                ('servicio_id', models.ForeignKey(blank=True, db_column='servicio_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='Ventas.servicio', verbose_name='Servicio')),
            ],
            options={
                'verbose_name': 'catalogo',
                'db_table': 'catalogo',
                'ordering': ['id_catalogo', 'servicio_id', 'fecha_creacion', 'fecha_actualizacion', 'estado'],
            },
        ),
        migrations.CreateModel(
            name='Calendario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia', models.DateField()),
                ('horaInicio', models.TimeField()),
                ('horaFin', models.TimeField()),
                ('cita_id', models.ForeignKey(db_column='cita_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='Ventas.cita')),
                ('cliente_id', models.ForeignKey(db_column='cliente_id', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cliente_calendario_id', to=settings.AUTH_USER_MODEL)),
                ('empleado_id', models.ForeignKey(db_column='empleado_id', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='empleado_calendario_id', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'calendario',
                'verbose_name_plural': 'calendario',
                'db_table': 'calendario',
            },
        ),
    ]
