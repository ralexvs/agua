from django.db import models
from django.db.models import Sum

#Para los signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.core.models import ClaseModelo
from apps.parametro.models import Servicio, Pago, Descuento, Multa, Tarifa


# Create your models here.

class Medidor(ClaseModelo):
    
    numero = models.CharField(verbose_name="Número medidor", max_length=50, unique=True)
    descripcion = models.CharField(verbose_name="Descripcion", max_length=254, null=True, blank=True)
    modelo = models.CharField(verbose_name="Modelo",
                              max_length=30, null=True, blank=True)
    lectura_inicial = models.IntegerField("lectura inicial", default=0)
    asignar = models.BooleanField("Asignar", default=False)
    
    class Meta:
        verbose_name_plural = 'Medidores'

    def __str__(self):
        return '{}'.format(str(self.numero))



class Barrio(ClaseModelo):

    descripcion = models.CharField(verbose_name="Descripcion", max_length=254)

    class Meta:
        verbose_name = 'Barrio'
        verbose_name_plural = 'Barrios'

    def __str__(self):
        return '{}'.format(self.descripcion)


class Abonado(ClaseModelo):
    
    identificacion = models.CharField("Identificación", max_length=13, unique=True)
    apellidos = models.CharField("Apellidos", max_length=50)
    nombres = models.CharField("Nombres", max_length=50)
    direccion = models.CharField(
        "Dirección", max_length=50, null=True, blank=True)
    email = models.EmailField("Correo", max_length=254, null=True, blank=True)
    web = models.URLField("Página Web", max_length=200, blank=True, null=True)
    telefono = models.CharField(
        "Teléfono", max_length=15, null=True, blank=True)
    celular = models.CharField("Celular", max_length=15, null=True, blank=True)
    fecha_nacimiento = models.DateField(verbose_name='Fecha de Nacimieno', null=True,blank=True)
    HOMBRE ='H'
    MUJER ='M'
    TIPO_SEXO = [
        (HOMBRE, 'Hombre'),
        (MUJER, 'Mujer')
        ]
    sexo = models.CharField("Sexo", max_length=50,
                            choices=TIPO_SEXO, default=HOMBRE)
    barrio = models.ForeignKey("barrio", verbose_name="Barrio / Sector", on_delete=models.CASCADE)
    foto = models.ImageField(verbose_name='Retrato', upload_to='parametro/abonado/', height_field=None, width_field=None, max_length=None, blank=True, null=True) 

    class Meta:

        verbose_name = "Abonado"
        verbose_name_plural = "Abonados"
        ordering =['apellidos']

    def __str__(self):

        return '{}{}{}'.format(self.apellidos, " ", self.nombres)

    def save(self):

        self.apellidos = self.apellidos.upper()
        self.nombres = self.nombres.upper()
        # Invoco al metodo save() del padre
        super(Abonado, self).save()


class Catastro(ClaseModelo):
    
    numero = models.IntegerField("Numero catastral", unique=True)
    fecha = models.DateTimeField("Fecha de Ingreso")
    abonado = models.ForeignKey("Abonado", verbose_name= "Abonado", on_delete=models.CASCADE)
    medidor = models.OneToOneField("Medidor", verbose_name="Medidor", on_delete=models.CASCADE)
    servicio = models.ForeignKey("parametro.Servicio", verbose_name="Servicio", on_delete=models.CASCADE)
    pago = models.ForeignKey("parametro.Pago", verbose_name="Forma de pago", on_delete=models.CASCADE)
    descuento = models.ForeignKey("parametro.Descuento", verbose_name="Descuento", on_delete=models.CASCADE)
    descripcion = models.CharField("descripcion", max_length=254, blank=True, null=True)
    suspender = models.BooleanField("Suspendido", default=False)
    NUEVO = 'NEW'
    ANTIGUO = 'ANT'
    NUEVO_COMUNIDAD ='NEW_COM'
    TIPO_PETICIONARIO = [
        (NUEVO, 'Nuevo'),
        (ANTIGUO, 'Antiguo'),
        (NUEVO_COMUNIDAD, 'Nuevo en la comunidad'),
    ]
    peticionario = models.CharField("Peticionario", max_length=7,
                                    choices=TIPO_PETICIONARIO, default=ANTIGUO)
    derecho_conexion = models.BooleanField("Derecho conexión", default=False)
    alcantarillado = models.BooleanField("Alcantarillado", default=False)
    class Meta:

        verbose_name = "Planilla catastral"
        verbose_name_plural = "Planillas Catastrales"
        ordering = ['-numero']
        
        
    def __str__(self):
        
        return '{}{}{}{}{}'.format(str(self.numero)," ", self.abonado.apellidos," " ,self.abonado.nombres)

    def save(self):
        if self.peticionario =='NEW':
            self.derecho_conexion = True
        elif self.peticionario == 'NEW_COM':
            self.derecho_conexion = True
        else:
            self.derecho_conexion = False

        # Invoco al metodo save() del padre
        super(Catastro, self).save()

class TipoLectura(ClaseModelo):
    
    descripcion = models.CharField("Descripción", max_length=50)

    class Meta:

        verbose_name = 'Tipo de lectura'
        verbose_name_plural = 'Tipos de lectruas'
        ordering = ['id']

    def __str__(self):

        return '{}'.format(self.descripcion)



class Lectura(ClaseModelo):

    periodo = models.DateField("Período consumo", unique=True)
    descripcion = models.CharField("Descripción", max_length=150)
    consumo_total = models.PositiveIntegerField("Consumo M3", default=0)
    total_base = models.DecimalField(
        "Tarifa base", max_digits=10, decimal_places=2, default=0)
    total_base_reserva = models.DecimalField(
        "Tarifa base reserva", max_digits=10, decimal_places=2, default=0)
    total_excedente = models.DecimalField(
        "Total excedente", max_digits=10, decimal_places=2, default=0)
    total_consumo_maximo = models.DecimalField(
        "Total consumo máximo", max_digits=10, decimal_places=2, default=0)
    total_administracion = models.DecimalField(
        "Administración", max_digits=10, decimal_places=2, default=0)
    total_alcantarillado = models.DecimalField(
        "Alcantarillado", max_digits=10, decimal_places=2, default=0)
    total_derecho_conexion = models.DecimalField(
        "Total derecho conexion", max_digits=10, decimal_places=2, default=0)
    total_otros = models.DecimalField(
        "Total otros valores", max_digits=10, decimal_places=2, default=0)
    total_general = models.DecimalField(
        "Total general", max_digits=10, decimal_places=2, default=0)

    class Meta:

        verbose_name = 'Lectura'
        verbose_name_plural = 'Lecturas'
        ordering = ['id']

    def __str__(self):
        return '{}'.format(self.periodo.strftime('%b/%Y'))
    
    def save(self):
        self.total_general = float(self.total_base) + \
            float(self.total_base_reserva) +  \
            float(self.total_excedente) + float(self.total_consumo_maximo) +\
            float(self.total_administracion) + float(self.total_alcantarillado) +\
            float(self.total_derecho_conexion) + float(self.total_otros)
        # Invoco al metodo save() del padre
        super(Lectura, self).save()

class LecturaDetalle(ClaseModelo):

    lectura = models.ForeignKey("Lectura", verbose_name="Lectura", on_delete=models.CASCADE)
    catastro = models.ForeignKey("Catastro", verbose_name="Clave catastral", on_delete=models.CASCADE)
    lectura_anterior = models.PositiveIntegerField("Lectura anterior")
    lectura_actual = models.PositiveIntegerField("Lectura actual")
    consumo = models.PositiveIntegerField("Consumo M3")
    tarifa = models.ForeignKey(Tarifa, verbose_name="Tarifa", on_delete=models.CASCADE)
    base = models.DecimalField("Tarifa base", max_digits=4, decimal_places=2, default=0)
    base_reserva = models.DecimalField("Tarifa base reserva", max_digits=4, decimal_places=2, default=0)
    tipo_lectura = models.ForeignKey("TipoLectura", verbose_name="Tipo de lectura", on_delete=models.CASCADE)
    valor_consumo_maximo = models.DecimalField("Valor consumo máximo", max_digits=10, decimal_places=2, default=0)
    valor_excedente = models.DecimalField("Valor por excedente", max_digits=10, decimal_places=2, default=0)
    administracion = models.DecimalField(
        "Administración", max_digits=10, decimal_places=2, default=0)
    alcantarillado = models.DecimalField(
        "Alcantarillado", max_digits=10, decimal_places=2, default=0)
    derecho_conexion = models.DecimalField(
        "Derecho conexión", max_digits=10, decimal_places=2, default=0)
    peticionario = models.CharField("Peticionario", max_length=7, null = True, blank=True)
    total = models.DecimalField("Total", max_digits=10, decimal_places=2, default=0)

    class Meta:

        verbose_name_plural = 'Detalle Lecturas'
        # Unique compuesto
        unique_together = ('lectura', 'catastro')

    def __str__(self):
        return str(self.lectura_anterior)

    def save(self):

        self.consumo = int(self.lectura_actual) - int(self.lectura_anterior)
        self.total = float(self.base)+float(self.base_reserva)+float(self.valor_excedente) + \
            float(self.valor_consumo_maximo)+float(self.administracion)+float(self.alcantarillado)+float(self.derecho_conexion)

        # Invoco al metodo save() del padre
        super(LecturaDetalle, self).save()


class MultaDetalle(ClaseModelo):

    lectura_detalle = models.ForeignKey(LecturaDetalle, verbose_name="Lectura Detalle", on_delete=models.CASCADE)
    lectura = models.IntegerField("Lectura")
    catastro = models.IntegerField("Catastro")
    multa = models.ForeignKey(Multa, verbose_name="Multa", on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField("Cantidad", default=1)
    valor = models.DecimalField("Valor", max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(
        "Valor", max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        verbose_name_plural = 'Detalle de multas'
        # Unique compuesto
        unique_together = ('lectura_detalle', 'multa')

    def __str__(self):
        return str(self.total)

    def save(self):
        self.total = int(self.cantidad) * float(self.valor)
        # Invoco al metodo save() del padre
        super(MultaDetalle, self).save()



#Signal ===============================================================================

#Signal LecturaDetalle ======================================================
@receiver(post_delete, sender=LecturaDetalle)
def letura_detalle_post_delete_receiver(sender, instance, **kwargs):

    lectura_id = instance.lectura.id
    id_medidor = instance.catastro.medidor.id
    id_catastro = instance.catastro.id

    enc = Lectura.objects.filter(pk=lectura_id).first()
    if enc:
        consumo_total = LecturaDetalle.objects.filter(lectura=lectura_id).aggregate(Sum('consumo'))
        total_base = LecturaDetalle.objects.filter(
            lectura=lectura_id).aggregate(Sum('base'))
        total_base_reserva = LecturaDetalle.objects.filter(
            lectura=lectura_id).aggregate(Sum('base_reserva'))
        total_excedente = LecturaDetalle.objects.filter(
            lectura=lectura_id).aggregate(Sum('valor_excedente'))
        total_consumo_maximo = LecturaDetalle.objects.filter(
            lectura=lectura_id).aggregate(Sum('valor_consumo_maximo'))
        total_administracion = LecturaDetalle.objects.filter(
            lectura=lectura_id).aggregate(Sum('administracion'))
        total_alcantarillado = LecturaDetalle.objects.filter(
            lectura=lectura_id).aggregate(Sum('alcantarillado'))
        total_derecho_conexion = LecturaDetalle.objects.filter(
            lectura=lectura_id).aggregate(Sum('derecho_conexion'))
        #total_general = LecturaDetalle.objects.filter(lectura=lectura_id).aggregate(Sum('total'))
        
        enc.consumo_total = consumo_total['consumo__sum']
        enc.total_base = total_base['base__sum']
        enc.total_base_reserva = total_base_reserva['base_reserva__sum']
        enc.total_excedente = total_excedente['valor_excedente__sum']
        enc.total_consumo_maximo = total_consumo_maximo['valor_consumo_maximo__sum']
        enc.total_administracion = total_administracion['administracion__sum']
        enc.total_alcantarillado = total_alcantarillado['alcantarillado__sum']
        enc.total_derecho_conexion = total_derecho_conexion['derecho_conexion__sum']
        #enc.total_general = total_general['total__sum']

        enc.save()

    med = Medidor.objects.filter(pk=id_medidor).first()
    if med:
        li = int(instance.lectura_anterior)
        med.lectura_inicial = li
        med.save()
    
    cat = Catastro.objects.filter(pk=id_catastro).first()
    if cat:
        peti = instance.peticionario
        cat.peticionario = peti
        cat.save()

@receiver(post_save, sender=LecturaDetalle)
def letura_detalle_post_save_receiver(sender, instance, **kwargs):

    lectura_id = instance.lectura.id
    id_medidor = instance.catastro.medidor.id
    id_catastro = instance.catastro.id

    enc = Lectura.objects.filter(pk=lectura_id).first()
    
    if enc:
        consumo_total = LecturaDetalle.objects.filter(
            lectura=lectura_id).aggregate(Sum('consumo'))
        total_base = LecturaDetalle.objects.filter(
            lectura=lectura_id).aggregate(Sum('base'))
        total_base_reserva = LecturaDetalle.objects.filter(
            lectura=lectura_id).aggregate(Sum('base_reserva'))
        total_excedente = LecturaDetalle.objects.filter(
            lectura=lectura_id).aggregate(Sum('valor_excedente'))
        total_consumo_maximo = LecturaDetalle.objects.filter(
            lectura=lectura_id).aggregate(Sum('valor_consumo_maximo'))
        total_administracion = LecturaDetalle.objects.filter(
            lectura=lectura_id).aggregate(Sum('administracion'))
        total_alcantarillado = LecturaDetalle.objects.filter(
            lectura=lectura_id).aggregate(Sum('alcantarillado'))
        total_derecho_conexion = LecturaDetalle.objects.filter(
            lectura=lectura_id).aggregate(Sum('derecho_conexion'))
        #total_general = LecturaDetalle.objects.filter(lectura=lectura_id).aggregate(Sum('total'))

        enc.consumo_total = consumo_total['consumo__sum']
        enc.total_base = total_base['base__sum']
        enc.total_base_reserva = total_base_reserva['base_reserva__sum']
        enc.total_excedente = total_excedente['valor_excedente__sum']
        enc.total_consumo_maximo = total_consumo_maximo['valor_consumo_maximo__sum']
        enc.total_administracion = total_administracion['administracion__sum']
        enc.total_alcantarillado = total_alcantarillado['alcantarillado__sum']
        enc.total_derecho_conexion = total_derecho_conexion['derecho_conexion__sum']
        #enc.total_general = total_general['total__sum']
        enc.save()

    med = Medidor.objects.filter(pk=id_medidor).first()
    if med:
        li = int(instance.lectura_actual)
        med.lectura_inicial = li
        med.save()
    
    cat = Catastro.objects.filter(pk=id_catastro).first()
    if cat:
        cat.peticionario = 'ANT'
        cat.save()

    
#Signal Catastro ======================================================
@receiver(post_save, sender=Catastro)
def catastro_post_save_receiver(sender, instance, **kwargs):

    id_medidor = instance.medidor.id

    med = Medidor.objects.filter(pk=id_medidor).first()
    if med:
        med.asignar = True
        med.save()

@receiver(post_delete, sender=Catastro)
def catastro_post_delete_receiver(sender, instance, **kwargs):

    id_medidor = instance.medidor.id

    med = Medidor.objects.filter(pk=id_medidor).first()
    if med:
        med.asignar = False
        med.save()


#Signal Multa Detalle ======================================================

@receiver(post_save, sender=MultaDetalle)
def multadetalle_post_save_receiver(sender, instance, **kwargs):
    total_otros=0

    id_lectura = instance.lectura_detalle.lectura.id
    id_lectura_detalle = instance.lectura_detalle.id
    
    lectura = Lectura.objects.filter(pk=id_lectura).first()
    if lectura:
        total_otros = MultaDetalle.objects.filter(
            lectura_detalle=id_lectura_detalle).aggregate(Sum('total'))
        total_otros = total_otros['total__sum']
        if total_otros==None:
            total_otros = 0
        
        lectura.total_otros = total_otros
            
        lectura.save()

@receiver(post_delete, sender=MultaDetalle)
def multadetalle_post_delete_receiver(sender, instance, **kwargs):
    total_otros=0

    id_lectura = instance.lectura_detalle.lectura.id
    id_lectura_detalle = instance.lectura_detalle.id
    
    lectura = Lectura.objects.filter(pk=id_lectura).first()
    if lectura:
        total_otros = MultaDetalle.objects.filter(
            lectura_detalle=id_lectura_detalle).aggregate(Sum('total'))
        total_otros = total_otros['total__sum']
        if total_otros==None:
            total_otros = 0
        
        lectura.total_otros = total_otros
            
        lectura.save()
