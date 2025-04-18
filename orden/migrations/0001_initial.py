# Generated by Django 4.2 on 2025-03-25 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vehiculo', '0001_initial'),
        ('cliente', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orden',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagenes', models.ImageField(blank=True, null=True, upload_to='Imagenes/', verbose_name='Imagenes del vehiculo')),
                ('modalidad', models.CharField(choices=[('particular', 'Particular'), ('terceros', 'Contra terceros'), ('riesgo', 'Contra todo riesgo'), ('recupero', 'Recupero de siniestro')], max_length=50, verbose_name='Modalidad de cobertura')),
                ('estado', models.CharField(blank=True, choices=[('espera', 'Esperando ingreso'), ('taller', 'En el taller'), ('entregado', 'Entregado')], max_length=50, null=True, verbose_name='Estado')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cliente.cliente', verbose_name='Cliente')),
                ('vehiculo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vehiculo.vehiculo', verbose_name='Vehiculo')),
            ],
            options={
                'verbose_name': 'orden',
                'verbose_name_plural': 'ordenes',
            },
        ),
    ]
