# Generated by Django 3.2.9 on 2022-03-28 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='cambios',
            fields=[
                ('id_cambios', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('Color_Letra', models.CharField(max_length=20)),
                ('Color_Fondo', models.CharField(max_length=20)),
                ('tamano_Titulo', models.CharField(max_length=20)),
                ('tamano_Texto', models.CharField(max_length=20)),
                ('Tipo_Letra', models.CharField(max_length=20)),
                ('Texto_Mision', models.CharField(max_length=500)),
                ('Texto_Vision', models.CharField(max_length=500)),
            ],
            options={
                'db_table': 'Cambios',
            },
        ),
        migrations.CreateModel(
            name='cambiosFooter',
            fields=[
                ('id_footer', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('Direccion', models.CharField(max_length=500)),
                ('Telefono', models.CharField(max_length=20)),
                ('Derechos', models.CharField(max_length=20)),
                ('Footer_Color_Letra', models.CharField(max_length=20)),
                ('Footer_Color_Fondo', models.CharField(max_length=20)),
                ('Footer_tamano_Titulo', models.CharField(max_length=20)),
                ('Footer_tamano_Texto', models.CharField(max_length=20)),
                ('Footer_Tipo_Letra', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'footer',
            },
        ),
        migrations.CreateModel(
            name='Permiso',
            fields=[
                ('id_permiso', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('nombre', models.CharField(max_length=40)),
                ('descripcion', models.TextField(max_length=250)),
                ('estado', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'permisos',
            },
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id_rol', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('nombre', models.CharField(max_length=40, unique=True)),
                ('descripcion', models.CharField(max_length=500)),
                ('estado', models.BooleanField(default=True)),
                ('permiso_id', models.ManyToManyField(db_column='permiso_id', to='Configuracion.Permiso')),
            ],
            options={
                'db_table': 'roles',
            },
        ),
    ]
