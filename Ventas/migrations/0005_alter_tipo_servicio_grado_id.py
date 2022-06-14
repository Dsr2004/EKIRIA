# Generated by Django 3.2.9 on 2022-06-14 03:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('Ventas', '0004_tipo_servicio_grado_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipo_servicio',
            name='grado_id',
            field=models.ForeignKey(db_column='grado_id', on_delete=django.db.models.deletion.CASCADE, to='auth.permission', verbose_name='Grado'),
        ),
    ]