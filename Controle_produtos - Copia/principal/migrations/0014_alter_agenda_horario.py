# Generated by Django 5.1.1 on 2024-12-06 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0013_alter_horario_hora_util'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agenda',
            name='horario',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
