# Generated by Django 2.2.3 on 2019-09-11 11:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catastro', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('parametro', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recaudacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True, verbose_name='Estado')),
                ('fc', models.DateTimeField(auto_now_add=True, verbose_name='Fecha creación')),
                ('fm', models.DateTimeField(auto_now=True, verbose_name='Fecha modificación')),
                ('um', models.IntegerField(blank=True, null=True, verbose_name='Usuario modifica')),
                ('fecha', models.DateField(verbose_name='Período consumo')),
                ('descripcion', models.CharField(max_length=150, verbose_name='Descripción')),
                ('total_consumo', models.PositiveIntegerField(blank=True, null=True, verbose_name='Consumo M3')),
                ('total_base', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Tarifa base')),
                ('total_base_reserva', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Tarifa base reserva')),
                ('total_excedente', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Total excedente')),
                ('total_consumo_maximo', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Total consumo máximo')),
                ('total_administracion', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Administración')),
                ('total_alcantarillado', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Alcantarillado')),
                ('total_derecho_conexion', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Total derecho conexion')),
                ('total_otros', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Total otros valores')),
                ('subtotal', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Subtotal')),
                ('total_descuento', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='T. descuento')),
                ('total_general', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Total general')),
                ('abonado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catastro.Abonado', verbose_name='Abonado')),
                ('descuento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parametro.Descuento', verbose_name='Descuento')),
                ('pago', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parametro.Pago', verbose_name='Pago')),
                ('uc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name_plural': 'Recaudaciones',
            },
        ),
        migrations.CreateModel(
            name='RecaudacionDetalle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True, verbose_name='Estado')),
                ('fc', models.DateTimeField(auto_now_add=True, verbose_name='Fecha creación')),
                ('fm', models.DateTimeField(auto_now=True, verbose_name='Fecha modificación')),
                ('um', models.IntegerField(blank=True, null=True, verbose_name='Usuario modifica')),
                ('catastro', models.IntegerField(verbose_name='Catastro')),
                ('lectura_anterior', models.PositiveIntegerField(verbose_name='Lectura anterior')),
                ('lectura_actual', models.PositiveIntegerField(verbose_name='Lectura actual')),
                ('consumo', models.PositiveIntegerField(verbose_name='Consumo M3')),
                ('base', models.DecimalField(decimal_places=2, default=0, max_digits=4, verbose_name='Tarifa base')),
                ('base_reserva', models.DecimalField(decimal_places=2, default=0, max_digits=4, verbose_name='Tarifa base reserva')),
                ('valor_consumo_maximo', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Valor consumo máximo')),
                ('valor_excedente', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Valor por excedente')),
                ('administracion', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Administración')),
                ('alcantarillado', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Alcantarillado')),
                ('derecho_conexion', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Derecho conexión')),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Total')),
                ('lectura_detalle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catastro.LecturaDetalle', verbose_name='Lectura detalle')),
                ('recaudacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recaudacion.Recaudacion', verbose_name='Recaudación')),
                ('uc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name_plural': 'Recaudaciones Detalle',
            },
        ),
        migrations.CreateModel(
            name='RecaudacionMultaDetalle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.BooleanField(default=True, verbose_name='Estado')),
                ('fc', models.DateTimeField(auto_now_add=True, verbose_name='Fecha creación')),
                ('fm', models.DateTimeField(auto_now=True, verbose_name='Fecha modificación')),
                ('um', models.IntegerField(blank=True, null=True, verbose_name='Usuario modifica')),
                ('recaudacion', models.IntegerField(verbose_name='Recaudación')),
                ('catastro', models.IntegerField(verbose_name='Catastro')),
                ('lectura', models.IntegerField(verbose_name='Lectura')),
                ('cantidad', models.PositiveIntegerField(default=1, verbose_name='Cantidad')),
                ('valor', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Valor')),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Valor')),
                ('multa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parametro.Multa', verbose_name='Multa')),
                ('multa_detalle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catastro.MultaDetalle', verbose_name='Multa detalle')),
                ('recaudacion_detalle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recaudacion.RecaudacionDetalle', verbose_name='Recaudacion detalle')),
                ('uc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name_plural': 'Detalle de multas recaudadas',
                'unique_together': {('multa_detalle', 'multa')},
            },
        ),
    ]
