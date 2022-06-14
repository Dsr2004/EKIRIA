# Generated by Django 3.2.9 on 2022-06-14 02:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('Ventas', '0003_alter_catalogo_servicio_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipo_servicio',
            name='grado_id',
            field=models.ForeignKey(default=120, on_delete=django.db.models.deletion.CASCADE, to='auth.permission', verbose_name='Grado'),
            preserve_default=False,
        ),
    ]