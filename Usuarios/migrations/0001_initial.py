# Generated by Django 3.2.9 on 2022-06-23 13:04

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CodigoPostal',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('cod_postal', models.CharField(max_length=15)),
            ],
            options={
                'db_table': 'Codigo_Postal',
            },
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id_municipio', models.AutoField(primary_key=True, serialize=False)),
                ('nom_municipio', models.CharField(max_length=60)),
                ('estado', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'municipios',
            },
        ),
        migrations.CreateModel(
            name='TipoDocumento',
            fields=[
                ('id_tipo_documento', models.AutoField(primary_key=True, serialize=False)),
                ('nom_tipo_documento', models.CharField(max_length=5)),
            ],
            options={
                'db_table': 'tipo_documento',
            },
        ),
        migrations.CreateModel(
            name='VistasDiarias',
            fields=[
                ('id_dia', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('Contador', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'VisitasDiarias',
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id_usuario', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('username', models.CharField(max_length=25, unique=True, verbose_name='Nombre de usuario')),
                ('nombres', models.CharField(max_length=60, verbose_name='Nombres')),
                ('apellidos', models.CharField(max_length=60, verbose_name='Apellidos')),
                ('telefono', models.CharField(blank=True, max_length=10, null=True, verbose_name='Número Télefonico')),
                ('celular', models.CharField(max_length=10, unique=True, verbose_name='Número De Celular')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Correo Electrónico')),
                ('fec_nac', models.DateField(verbose_name='Fecha De Nacimiento')),
                ('num_documento', models.CharField(max_length=10, unique=True, verbose_name='Número De Identificación')),
                ('img_usuario', models.ImageField(default='perfil/profile.jpg', max_length=200, upload_to='perfil/', verbose_name='Imagen De Perfil')),
                ('direccion', models.CharField(blank=True, max_length=250, null=True)),
                ('estado', models.BooleanField(default=True)),
                ('administrador', models.BooleanField(default=False)),
                ('cod_postal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Usuarios.codigopostal')),
                ('municipio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Usuarios.municipio')),
                ('rol', models.ForeignKey(blank=True, default=2, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='auth.group')),
                ('tipo_documento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Usuarios.tipodocumento')),
            ],
            options={
                'db_table': 'usuarios',
                'permissions': [('Empleado', 'Es un empleado'), ('Cliente', 'Es un cliente'), ('Administrador', 'Es un administrador'), ('Grado 1', 'Puede visualizar elementos de grado 1'), ('Grado 2', 'Puede visualizar elementos de grado 2'), ('Grado 3', 'Puede visualizar elementos de grado 3'), ('Grado 4', 'Puede visualizar elementos de grado 4'), ('Grado 5', 'Puede visualizar elementos de grado 5'), ('Grado 6', 'Puede visualizar elementos de grado 6'), ('Grado 7', 'Puede visualizar elementos de grado 7'), ('Grado 8', 'Puede visualizar elementos de grado 8'), ('Grado 9', 'Puede visualizar elementos de grado 9'), ('Grado 10', 'Puede visualizar elementos de grado 10')],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id_post', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('titulo', models.CharField(max_length=100, verbose_name='Titulo')),
                ('image', models.ImageField(upload_to='pos/')),
                ('text', models.TextField(verbose_name='Texto')),
                ('time', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Usuarios.usuario')),
            ],
        ),
    ]
