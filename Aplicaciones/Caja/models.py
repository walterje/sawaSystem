from email.policy import default
from django.db import models
from datetime import datetime
from django.forms import model_to_dict
from Aplicaciones.User.models import *
# Create your models here.

class Moneda(models.Model):
    descripcion=models.CharField(max_length=15,unique=True)
    sigla=models.CharField(max_length=10,unique=True)

    def __str__(self):
        return self.sigla
    
    def toJSON(self):
        item=model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Moneda'
        verbose_name_plural = 'Monedas'
        db_table = 'moneda'
        ordering = ['id']


class Caja(models.Model):
    estados = (
        ('0', 'Abierta'),
        ('1', 'Cerrada'),
        
    )
    nombre = models.CharField(max_length=10, unique=True,verbose_name= "Nombre")
    estado=models.CharField(max_length=1, choices=estados,default='1') 
    #fecha = models.DateField(default=datetime.now, verbose_name="Fecha")
    moneda = models.ForeignKey(Moneda,blank=False,null=False,on_delete=models.PROTECT)
    #descripcion=models.CharField(max_length=15,unique=True,null=True)
    #user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    saldo_actual=models.BigIntegerField(default=0)
    monto_inicio=models.BigIntegerField(default=0)
    monto_cierre=models.BigIntegerField(default=0)
    total_ingreso=models.BigIntegerField(default=0)
    total_egreso=models.BigIntegerField(default=0)
  
    def __str__(self):
        return self.nombre
        
    def toJSON(self):
        item=model_to_dict(self)
        item['moneda']=self.moneda.toJSON()
        item['estado']=self.estado
        item['nombre']=self.nombre
        item['saldo_actual'] = format(self.saldo_actual)
        item['monto_inicio'] = format(self.monto_inicio)
        item['monto_cierre'] = format(self.monto_cierre)
        item['total_ingreso'] = format(self.total_ingreso)
        item['total_egreso'] = format(self.total_egreso)
        return item

    class Meta:
        verbose_name = 'Caja'
        verbose_name_plural = 'Cajas'
        db_table = 'caja'
        ordering = ['id']  
    

class MovimientoCaja (models.Model):
    tipo_mov= (
        ('0', 'Entrada'),
        ('1', 'Salida'),
    )
    caja=models.ForeignKey(Caja,blank=False,null=False,on_delete=models.PROTECT)
    fecha_movimiento=models.DateField(default=datetime.now, verbose_name="Fecha Mov_Caja")
    #moneda=models.ForeignKey(Moneda,blank=False,null=False,on_delete=models.PROTECT)
    #monto_movimiento=models.BigIntegerField(default=0)
    descripcion=models.CharField(max_length=30)
    tipo_movimiento=models.CharField(max_length=1, choices=tipo_mov)
    monto_ingreso=models.BigIntegerField(default=0)
    monto_egreso=models.BigIntegerField(default=0)
    monto_inicio=models.BigIntegerField(default=0)
    monto_cierre=models.BigIntegerField(default=0)

    def __str__(self):
        return self.descripcion
        
    def toJSON(self):
        item=model_to_dict(self) 
        item['caja']=self.caja.toJSON()
        item['fecha_movimiento'] = self.fecha_movimiento.strftime('%Y-%m-%d')
        #item['monto_movimiento'] = format(self.monto_movimiento)
        item['descripcion']=self.descripcion
        item['tipo_movimiento']=self.tipo_movimiento
        item['monto_ingreso'] = format(self.monto_ingreso)
        item['monto_egreso'] = format(self.monto_egreso)
        item['monto_inicio'] = format(self.monto_inicio)
        item['monto_cierre'] = format(self.monto_cierre)
        return item

    class Meta:
        verbose_name = 'Movimiento Caja'
        verbose_name_plural = 'Movimientos Cajas'
        db_table = 'movimiento_caja'
        ordering = ['id']  


#Forma pago
class FormaPago(models.Model):
    descripcion=models.CharField(max_length=15,unique=True)

    def __str__(self):
        return self.descripcion
    
    def toJSON(self):
        item=model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'forma_pago'
        verbose_name_plural = 'Formas de Pagos'
        db_table = 'forma_pago'
        ordering = ['id']