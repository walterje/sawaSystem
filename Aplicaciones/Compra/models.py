from msilib.schema import Class
from pyexpat import model
from django.db import models
from django.forms import model_to_dict
from datetime import datetime
from Aplicaciones.Producto.models import Producto
from Aplicaciones.Caja.models import *
from Aplicaciones.Venta.models import *
from Aplicaciones.User.models import *
# Create your models here.
# Proveedor
class Proveedor(models.Model):
    nombre = models.CharField(max_length=50, unique=True,verbose_name= "Nombre")
    ruc = models.CharField(max_length=10,unique=True)
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=100)
    email = models.EmailField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nombre    
    
    def get_proveedor (self):
        return '{} / {}'.format(self.nombre, self.ruc)

    

    
    def toJSON(self):
        item=model_to_dict(self)
        item['prov']=self.get_proveedor()
        return item

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        db_table = 'proveedor'
        ordering = ['id']

#Orden de Compra
class OrdenCompra(models.Model):
    fecha_orden = models.DateField(default=datetime.now, verbose_name="Fecha Orden")
    #fecha_entrega= models.DateField(default=datetime.now, verbose_name="Fecha Entrega")
    proveedor = models.ForeignKey(Proveedor,blank=False,null=False,on_delete=models.PROTECT)
    estados = (
        ('0', 'Pendiente'),
        ('1', 'Confirmado'),
        ('2', 'Anulado'),
        ('3', 'Cerrada'),
    )
    estado = models.CharField(max_length=1, choices=estados, default='0') 
    subtotal = models.BigIntegerField(default=0)
    iva_0 = models.BigIntegerField(default=0)
    iva_5 = models.BigIntegerField(default=0)
    iva_10 = models.BigIntegerField(default=0)
    total = models.BigIntegerField(default=0)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
  
    def __str__(self):
        return self.proveedor.nombre
    # para que se cree una relacion con la compañia  
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if Company.objects.all().exists():
            self.company = Company.objects.first()
        super(OrdenCompra, self).save()
        
    def toJSON(self):
        item=model_to_dict(self)
        item['proveedor']=self.proveedor.toJSON()
        item['estado']=self.estado
        item['subtotal'] = format(self.subtotal)
        item['iva_0'] = format(self.iva_0)
        item['iva_5'] = format(self.iva_5)
        item['iva_10'] = format(self.iva_10)
        item['total'] = format(self.total)
        item['fecha_orden']=self.fecha_orden.strftime('%Y-%m-%d')
        item['det']=[i.toJSON() for i in self.ordencompradet_set.all()]
        return item

    class Meta:
        verbose_name = 'Orden'
        verbose_name_plural = 'Ordenes'
        db_table = 'ordenCompra'
        ordering = ['id']

#Detalle del orden
class OrdenCompraDet(models.Model):
    nro_orden_c = models.ForeignKey(OrdenCompra,blank=False,null=False,on_delete=models.PROTECT)
    producto = models.ForeignKey(Producto,blank=False,null=False,on_delete=models.PROTECT)
    precio = models.BigIntegerField(default=0)
    cantidad = models.PositiveIntegerField()
    subtotal = models.BigIntegerField(default=0)


    def __str__(self):
        return str(self.id)

    def toJSON(self):
        item=model_to_dict(self,exclude=['nro_orden_c']) 
        item['producto']=self.producto.toJSON()
        item['precio'] = format(self.precio)
        item['subtotal'] = format(self.subtotal)
        return item

    class Meta:
        verbose_name = 'Orden Compra Det'
        verbose_name_plural = 'Ordenes de Compras Det'
        db_table = 'orden_compra_det'
        ordering = ['id']

#Compras
class Compra(models.Model):
    ordenCompra = models.ForeignKey(OrdenCompra,blank=False,null=False,on_delete=models.PROTECT)
    fecha_compra = models.DateField(default=datetime.now, verbose_name="Fecha Compra")
    nro_factura = models.CharField(max_length=20,verbose_name="Factura Compra")
    tipo = (
        ('0', 'Contado'),
        ('1', 'Credito'),
    )
    tipo_compra = models.CharField(max_length=1, choices=tipo, verbose_name="Tipo Compra") 
    fecha_plazo = models.DateField(default=datetime.now, verbose_name="Fecha Plazo")
    proveedor = models.ForeignKey(Proveedor,blank=False,null=False,on_delete=models.PROTECT)
    subtotal = models.BigIntegerField(default=0)
    iva_0 = models.BigIntegerField(default=0)
    iva_5 = models.BigIntegerField(default=0)
    iva_10 = models.BigIntegerField(default=0)
    total = models.BigIntegerField(default=0)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.proveedor.nombre
    
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if Company.objects.all().exists():
            self.company = Company.objects.first()
        super(Compra, self).save()
    
    def toJSON(self):
        item=model_to_dict(self)
        item['ordenCompra']=self.ordenCompra.toJSON()
        item['fecha_compra']=self.fecha_compra.strftime('%Y-%m-%d')
        item['nro_factura']=self.nro_factura
        item['tipo_compra']=self.tipo_compra
        item['fecha_plazo']=self.fecha_plazo.strftime('%Y-%m-%d')
        item['proveedor']=self.proveedor.toJSON()
        item['subtotal'] = format(self.subtotal)
        item['iva_0'] = format(self.iva_0)
        item['iva_5'] = format(self.iva_5)
        item['iva_10'] = format(self.iva_10)
        item['total'] = format(self.total)
        item['det']=[i.toJSON() for i in self.comprasdet_set.all()]
        return item

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
        db_table = 'compra'
        ordering = ['id']

#Compras detalle
class ComprasDet(models.Model):
    compra = models.ForeignKey(Compra,blank=False,null=False,on_delete=models.PROTECT)
    producto = models.ForeignKey(Producto,blank=False,null=False,on_delete=models.PROTECT)
    precio = models.BigIntegerField(default=0)
    cantidad = models.PositiveIntegerField()
    subtotal = models.BigIntegerField(default=0)


    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Compra Det'
        verbose_name_plural = 'Compras Det'
        db_table = 'compra_det'
        ordering = ['id']
    
    def toJSON(self):
        item=model_to_dict(self,exclude=['compra']) 
        item['producto']=self.producto.toJSON()
        item['precio'] = format(self.precio)
        item['subtotal'] = format(self.subtotal)
        return item

#Cuentas por pagar
class CuentaXpagar(models.Model):
    compra = models.ForeignKey(Compra,blank=False,null=False,on_delete=models.PROTECT)
    estadoCuenta = (
        ('0', 'Pagado'),
        ('1', 'Deuda'),
    )
    estado = models.CharField(max_length=1, choices=estadoCuenta, default='0') 
    monto_x_pagar = models.BigIntegerField(default=0)
    saldo = models.BigIntegerField(default=0)

    def __str__(self):
        return str(self.compra.proveedor.nombre)

    def toJSON(self):
        item=model_to_dict(self)
        item['compra']=self.compra.toJSON()
        item['estado']=self.estado
        item['monto_x_pagar'] = format(self.monto_x_pagar)
        item['saldo'] = format(self.saldo)
        return item

    class Meta:
        verbose_name = 'Cuenta por pagar'
        verbose_name_plural = 'Cuentas por pagar'
        db_table = 'cuenta_x_pagar'
        ordering = ['id']

#pago
class Pago(models.Model):
    cuenta_x_pagar = models.ForeignKey(CuentaXpagar,blank=False,null=False,on_delete=models.PROTECT)
    fecha_pago = models.DateField(default=datetime.now, verbose_name="Fecha pago")
    monto_pagado = models.BigIntegerField(default=0)
    #moneda = models.ForeignKey(Moneda,blank=False,null=False,on_delete=models.PROTECT,default='GS.')
    caja = models.ForeignKey(Caja,blank=False,null=False,on_delete=models.PROTECT,default='1')
    forma_pago = models.ForeignKey(FormaPago,blank=False,null=False,on_delete=models.PROTECT,default='1')
    efectivo = models.BigIntegerField(default=0)
    vuelto = models.BigIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return str(self.id)
    
    def toJSON(self):
        item=model_to_dict(self)
        item['cuenta_x_pagar']=self.cuenta_x_pagar.toJSON()
        item['caja']=self.caja.toJSON()
        item['forma_pago']=self.forma_pago.toJSON()
        item['user']=self.user.toJSON()
        item['fecha_pago']=self.fecha_pago.strftime('%Y-%m-%d')
        item['monto_pagado'] = format(self.monto_pagado)
        item['efectivo'] = format(self.efectivo)
        item['vuelto'] = format(self.vuelto)
        return item

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Cuentas pagadas'
        db_table = 'pago'
        ordering = ['id']

