# Generated by Django 3.2.9 on 2022-06-27 23:50

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notificacion',
            fields=[
                ('id_notificacion', models.AutoField(primary_key=True, serialize=False)),
                ('verbo', models.CharField(max_length=220)),
                ('fecha', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('leido', models.BooleanField(default=False)),
                ('direct', models.CharField(blank=True, max_length=200, null=True)),
                ('object_id_actor', models.PositiveIntegerField()),
                ('actor_content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notificar_actor', to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'notificacion',
                'verbose_name_plural': 'notificiaciones',
                'db_table': 'notificaciones',
                'abstract': False,
            },
        ),
    ]
