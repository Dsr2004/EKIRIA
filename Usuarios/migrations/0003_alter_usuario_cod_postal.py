# Generated by Django 3.2.9 on 2022-05-25 14:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Usuarios', '0002_auto_20220525_0910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='cod_postal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Usuarios.codigopostal'),
        ),
    ]