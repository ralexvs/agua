from django.db import models
from apps.core.models import ClaseModelo
from apps.catastro.models import LecturaDetalle, Catastro, Abonado, MultaDetalle
from apps.parametro.models import Servicio, Tarifa, Pago,Descuento, Multa

#Para los signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver



# Create your models here.

class Recaudacion(ClaseModelo):

    fecha = models.DateField("Período consumo")
    abonado = models.ForeignKey("catastro.Abonado", verbose_name="Abonado", on_delete=models.CASCADE)
    descripcion = models.CharField("Descripción", max_length=150)
    pago = models.ForeignKey("parametro.Pago", verbose_name="Pago", on_delete=models.CASCADE)
    descuento = models.ForeignKey("parametro.Descuento", verbose_name="Descuento", on_delete=models.CASCADE)
    total_consumo = models.PositiveIntegerField("Consumo M3", null=True, blank=True)
    total_base = models.DecimalField("Tarifa base", max_digits=10, decimal_places=2, null=True, blank=True)
    total_base_reserva = models.DecimalField("Tarifa base reserva", max_digits=10, decimal_places=2, null=True, blank=True)
    total_excedente = models.DecimalField("Total excedente", max_digits=10, decimal_places=2, null=True, blank=True)
    total_consumo_maximo = models.DecimalField("Total consumo máximo", max_digits=10, decimal_places=2, null=True, blank=True)
    total_administracion = models.DecimalField(
        "Administración", max_digits=10, decimal_places=2, default=0)
    total_alcantarillado = models.DecimalField(
        "Alcantarillado", max_digits=10, decimal_places=2, default=0)
    total_derecho_conexion = models.DecimalField(
        "Total derecho conexion", max_digits=10, decimal_places=2, default=0)
    total_otros = models.DecimalField("Total otros valores", max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField("Subtotal", max_digits=10, decimal_places=2, null=True, blank=True)
    total_descuento = models.DecimalField("T. descuento", max_digits=10, decimal_places=2, null=True, blank=True)
    total_general = models.DecimalField("Total general", max_digits=10, decimal_places=2, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Recaudaciones"

    def __str__(self):
        return self.descripcion

    def save(self):
  
        self.subtotal = float(self.total_base) + float(self.total_base_reserva) + float(
            self.total_excedente) + float(self.total_consumo_maximo) + float(self.total_administracion) + float(self.total_alcantarillado) + float(self.total_derecho_conexion) + float(self.total_otros)
        self.total_general = float(self.subtotal)-float(self.total_descuento)

        # Invoco al metodo save() del padre
        super(Recaudacion, self).save()

class RecaudacionDetalle(ClaseModelo):
    
    recaudacion = models.ForeignKey("Recaudacion", verbose_name="Recaudación", on_delete=models.CASCADE)
    lectura_detalle = models.ForeignKey("catastro.LecturaDetalle", verbose_name="Lectura detalle", on_delete=models.CASCADE)
    catastro = models.IntegerField("Catastro")
    lectura_anterior = models.PositiveIntegerField("Lectura anterior")
    lectura_actual = models.PositiveIntegerField("Lectura actual")
    consumo = models.PositiveIntegerField("Consumo M3")
    base = models.DecimalField(
        "Tarifa base", max_digits=4, decimal_places=2, default=0)
    base_reserva = models.DecimalField(
        "Tarifa base reserva", max_digits=4, decimal_places=2, default=0)
    valor_consumo_maximo = models.DecimalField(
        "Valor consumo máximo", max_digits=10, decimal_places=2, default=0)
    valor_excedente = models.DecimalField("Valor por excedente", max_digits=10, decimal_places=2, default=0)
    administracion = models.DecimalField(
        "Administración", max_digits=10, decimal_places=2, default=0)
    alcantarillado = models.DecimalField(
        "Alcantarillado", max_digits=10, decimal_places=2, default=0)
    derecho_conexion = models.DecimalField(
        "Derecho conexión", max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField("Total", max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        verbose_name_plural = "Recaudaciones Detalle"

    def __str__(self):
        return str(self.recaudacion)

    def save(self):
    
        self.total = float(self.base) + float(self.base_reserva) + \
            float(self.valor_excedente) + float(self.valor_consumo_maximo) + \
            float(self.administracion) + \
            float(self.alcantarillado) + float(self.derecho_conexion)

        # Invoco al metodo save() del padre
        super(RecaudacionDetalle, self).save()


class RecaudacionMultaDetalle(ClaseModelo):
    recaudacion = models.IntegerField("Recaudación")
    recaudacion_detalle = models.ForeignKey(RecaudacionDetalle, verbose_name="Recaudacion detalle", on_delete=models.CASCADE)
    multa_detalle = models.ForeignKey(MultaDetalle, verbose_name="Multa detalle", on_delete=models.CASCADE)
    catastro = models.IntegerField("Catastro")
    multa = models.ForeignKey(Multa, verbose_name="Multa", on_delete=models.CASCADE)
    lectura = models.IntegerField("Lectura")
    cantidad = models.PositiveIntegerField("Cantidad", default=1)
    valor = models.DecimalField("Valor", max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField("Valor", max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        verbose_name_plural = 'Detalle de multas recaudadas'
        # Unique compuesto
        unique_together = ('multa_detalle', 'multa')

    def __str__(self):
        return str(self.total)

    def save(self):
        self.total = int(self.cantidad) * float(self.valor)
        # Invoco al metodo save() del padre
        super(RecaudacionMultaDetalle, self).save()


#Signal Recaudacion ======================================================
@receiver(post_save, sender=RecaudacionDetalle)
def recaudaciondetalle_post_save_receiver(sender, instance, **kwargs):

    id_lecturadetalle = instance.lectura_detalle.id

    detLec = LecturaDetalle.objects.filter(pk=id_lecturadetalle).first()
    if detLec:
        detLec.estado = False
        detLec.save()

#Signal RecaudacionMultaDetalle ======================================================
@receiver(post_save, sender=RecaudacionMultaDetalle)
def recaudacionmultadetalle_post_save_receiver(sender, instance, **kwargs):

    id_multadetalle = instance.multa_detalle.id
    print("Multa detalle id", id_multadetalle)
    rmd = MultaDetalle.objects.filter(pk=id_multadetalle).first()
    if rmd:
        rmd.estado = False
        rmd.save()
