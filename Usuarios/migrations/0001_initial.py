<<<<<<< HEAD
# Generated by Django 3.2.9 on 2022-04-23 23:55
=======
# Generated by Django 3.2.9 on 2022-04-25 11:19
>>>>>>> 1e8314f8530d53974dfab999b26417559dce7645

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
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
                ('celular', models.CharField(max_length=10, verbose_name='Número De Celular')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Correo Electrónico')),
                ('fec_nac', models.DateField(verbose_name='Fecha De Nacimiento')),
                ('num_documento', models.CharField(max_length=10, unique=True, verbose_name='Número De Identificación')),
                ('img_usuario', models.ImageField(default='perfil/profile.jpg', max_length=200, upload_to='perfil/', verbose_name='Imagen De Perfil')),
                ('direccion', models.CharField(blank=True, max_length=250, null=True)),
                ('cod_postal', models.CharField(max_length=20, null=True)),
                ('estado', models.BooleanField(default=True)),
                ('administrador', models.BooleanField(default=False)),
                ('municipio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Usuarios.municipio')),
                ('rol', models.ForeignKey(blank=True, default=2, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
                ('tipo_documento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Usuarios.tipodocumento')),
            ],
            options={
                'db_table': 'usuarios',
            },
        ),
        migrations.CreateModel(
            name='Notificacion',
            fields=[
                ('id_notificacion', models.AutoField(primary_key=True, serialize=False)),
                ('mensaje', models.CharField(max_length=1000)),
                ('usuario_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'notificacion',
                'verbose_name_plural': 'notificiaciones',
                'db_table': 'notificaciones',
            },
        ),
    ]
