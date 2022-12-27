from datetime import datetime
from django.db import models
from django.forms import model_to_dict
# Create your models here.

# Tipo Producto
class TipoProducto(models.Model):
    nombre = models.CharField(max_length=50,verbose_name="Nombre ",unique=True)
    
    def __str__(self):
         return "{0}".format(self.nombre)

    #ajax
    def toJSON(self):
        item=model_to_dict(self)
        return item

    class Meta:
        verbose_name= 'Tipo Producto'
        verbose_name_plural = 'Tipos Productos'
        db_table='tipo_producto'
        ordering = ['id']


# Producto
class Producto(models.Model):
    tipo_producto = models.ForeignKey(TipoProducto,blank=False,null=False,on_delete=models.PROTECT)
    nombre_producto = models.CharField(max_length=150,verbose_name="Nombre",unique=True)
    cant_stock = models.PositiveIntegerField(default=0, verbose_name='Stock')
    stock_minimo = models.PositiveIntegerField(default=1, verbose_name='Stock Minimo')
    precio_compra = models.BigIntegerField(default=0, verbose_name='Precio compra')
    precio_venta = models.BigIntegerField(default=0, verbose_name='Precio venta')
    tipos_impuestos = (
        ('0', '0%'),
        ('1', '5%'),
        ('2', '10%')
    )
    iva = models.CharField(max_length=1, choices=tipos_impuestos, default='2') 
    
    
    def __str__(self):
        return self.nombre_producto
    
    def toJSON(self):
        item=model_to_dict(self)
        item['tipo_producto'] = self.tipo_producto.toJSON()
        item['precio_compra'] = format(self.precio_compra)
        item['precio_venta'] = format(self.precio_venta)
        return item

    class Meta:
        verbose_name ='Producto'
        verbose_name_plural ='Productos'
        db_table = 'producto'
        ordering = ['id']

#Stock
class Stock(models.Model):
    producto = models.ForeignKey(Producto,blank=False,null=False,on_delete=models.PROTECT)
    cant_actual = models.PositiveIntegerField(null=True)
    cant_minimo = models.PositiveIntegerField(default=1, verbose_name='Stock Minimo')
        
    def __str__(self):
         return "{0}".format(self.producto.nombre_producto)

    #ajax
    def toJSON(self):
        item=model_to_dict(self)
        return item

    class Meta:
        verbose_name= 'Stock'
        verbose_name_plural = 'Stocks'
        db_table='stock'
        ordering = ['id']

#Precio
class Precio(models.Model):
    producto = models.ForeignKey(Producto,blank=False,null=False,on_delete=models.PROTECT)
    fecha_Compra = models.DateField(default=datetime.now, verbose_name='Fecha de Compra')
    precio_compra = models.PositiveIntegerField(default=0, verbose_name='Precio compra')
    
    def __str__(self):
         return "{0}".format(self.producto.nombre_producto)

    #ajax
    def toJSON(self):
        item=model_to_dict(self)
        return item

    class Meta:
        verbose_name= 'Precio'
        verbose_name_plural = 'Precios'
        db_table='precio'
        ordering = ['id']


class MovimientoStock (models.Model):
    tipo_mov= (
        ('0', 'Entrada'),
        ('1', 'Salida'),
    )
    producto=models.ForeignKey(Producto,blank=False,null=False,on_delete=models.PROTECT)
    fecha_mov=models.DateField(default=datetime.now, verbose_name="Fecha Mov_Prod")
    cant_mov=models.BigIntegerField(default=0)
    descripcion=models.CharField(max_length=30)
    tipo_movimiento=models.CharField(max_length=1, choices=tipo_mov,default='1')
   

    def __str__(self):
        return self.descripcion
        
    def toJSON(self):
        item=model_to_dict(self) 
        item['prod']=self.producto.toJSON()
        item['fecha_mov'] = self.fecha_mov.strftime('%Y-%m-%d')
        item['cant_mov'] = format(self.cant_mov)
        item['descripcion']=self.descripcion
        item['tipo_movimiento']=self.tipo_movimiento
        return item

    class Meta:
        verbose_name = 'Movimiento Stock'
        verbose_name_plural = 'Movimientos Stock'
        db_table = 'movimiento_stock'
        ordering = ['id']  

