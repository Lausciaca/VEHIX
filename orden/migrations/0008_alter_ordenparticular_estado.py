# Generated by Django 4.2 on 2025-03-28 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orden', '0007_ordenparticular_ordenrecupero_ordenriesgo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordenparticular',
            name='estado',
            field=models.CharField(blank=True, choices=[('1', 'Presupusto'), ('2', 'Enviar a cliente'), ('3', 'Acordar turno'), ('4', 'Ingresar al taller'), ('5', 'Entregar el vehiculo')], max_length=50, null=True, verbose_name='Estado'),
        ),
    ]
