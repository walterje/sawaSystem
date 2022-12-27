from django.db import models
from django.forms import model_to_dict
from datetime import datetime
from SAWA_SYS import settings
from Aplicaciones.Producto.models import Producto
from Aplicaciones.Caja.models import *
from Aplicaciones.User.models import *
# Create your models here.
#cliente
class Cliente(models.Model):
    nombre = models.CharField(max_length=150, verbose_name='Nombres')
    apellido= models.CharField(max_length=150, verbose_name='Apellido')
    ci = models.CharField(max_length=20, unique=True, verbose_name='CI/RUC')
    direccion = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    sexo_choices= (('M','Masculino'),('F','Femenino'),)
    sexo = models.CharField(max_length=10, choices=sexo_choices, default='M', verbose_name='Sexo')
    telefono = models.CharField(max_length=20)
    def __str__(self):
        return self.get_nombre_completo()
    
    def get_nombre_completo (self):
        return '{} {} / {}'.format(self.nombre, self.apellido, self.ci)

    def toJSON(self):
        item = model_to_dict(self)
        item['cli'] = '{} {}'.format(self.nombre, self.apellido)
        item['nombre_completo'] = self.get_nombre_completo()
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        db_table = 'cliente'
        ordering = ['id']

#Compañia
class Company(models.Model):
    nombre = models.CharField(max_length=150, verbose_name='Nombre')
    ruc = models.CharField(max_length=12, verbose_name='Ruc')
    direccion = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    celular = models.CharField(max_length=15, verbose_name='Celular')
    telefono = models.CharField(max_length=15, verbose_name='Teléfono')
    email = models.EmailField(max_length=50, blank=True, null=True)
    timbrado= models.CharField(max_length=8, verbose_name='Timbrado',blank=True, null=True)
    fecha_desde = models.DateField(default=datetime.now, verbose_name="Fecha desde",blank=True, null=True)
    fecha_hasta = models.DateField(default=datetime.now, verbose_name="Fecha hasta",blank=True, null=True)
    image = models.ImageField(upload_to='company/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')


    def __str__(self):
        return self.nombre

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/ps.png'

    def toJSON(self):
        item = model_to_dict(self)
        item['image'] = self.get_image()
        return item

    class Meta:
        verbose_name = 'Compañia'
        verbose_name_plural = 'Compañias'
        db_table = 'company'
        default_permissions = ()
        permissions = (
            ('change_company', 'Can change Company'),
        )
        ordering = ['id']


#Orden de venta
class OrdenVenta(models.Model):
    fecha_orden_v = models.DateField(default=datetime.now, verbose_name="Fecha Orden Venta")
    #fecha_entrega= models.DateField(default=datetime.now, verbose_name="Fecha Entrega")
    cliente = models.ForeignKey(Cliente,blank=False,null=False,on_delete=models.PROTECT)
    estados = (
        ('0', 'Pendiente'),
        ('1', 'Confirmado'),
        ('2', 'Anulado'),
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
        return self.cliente.nombre
    
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if Company.objects.all().exists():
            self.company = Company.objects.first()
        super(OrdenVenta, self).save()
        
        
    def toJSON(self):
        item=model_to_dict(self)
        item['cliente']=self.cliente.toJSON()
        item['estado']=self.estado
        item['subtotal'] = format(self.subtotal)
        item['iva_0'] = format(self.iva_0)
        item['iva_5'] = format(self.iva_5)
        item['iva_10'] = format(self.iva_10)
        item['total'] = format(self.total)
        item['fecha_orden_v']=self.fecha_orden_v.strftime('%Y-%m-%d')
        item['det']=[i.toJSON() for i in self.ordenventadet_set.all()]
        return item

    class Meta:
        verbose_name = 'Orden Venta'
        verbose_name_plural = 'Ordenes de Ventas'
        db_table = 'orden_venta'
        ordering = ['id']

#Detalle de la orden de Venta
class OrdenVentaDet(models.Model):
    nro_orden_v = models.ForeignKey(OrdenVenta,blank=False,null=False,on_delete=models.PROTECT)
    producto = models.ForeignKey(Producto,blank=False,null=False,on_delete=models.PROTECT)
    precio_venta = models.BigIntegerField(default=0)
    cantidad = models.PositiveIntegerField()
    subtotal = models.BigIntegerField(default=0)


    def __str__(self):
        return str(self.id)

    def toJSON(self):
        item=model_to_dict(self,exclude=['nro_orden_v']) 
        item['producto']=self.producto.toJSON()
        item['precio_venta'] = format(self.precio_venta)
        item['subtotal'] = format(self.subtotal)
        return item

    class Meta:
        verbose_name = 'Orden Venta Det'
        verbose_name_plural = 'Ordenes de Ventas Det'
        db_table = 'orden_venta_det'
        ordering = ['id']
    
#Ventas
class Venta(models.Model):
    ordenVenta = models.ForeignKey(OrdenVenta,blank=False,null=False,on_delete=models.PROTECT)
    fecha_venta = models.DateField(default=datetime.now, verbose_name="Fecha Venta")
    tipo = (
        ('0', 'Contado'),
        ('1', 'Credito'),
    )
    tipo_venta= models.CharField(max_length=1, choices=tipo, verbose_name="Tipo Venta") 
    fecha_plazo = models.DateField(default=datetime.now, verbose_name="Fecha Plazo")
    cliente = models.ForeignKey(Cliente,blank=False,null=False,on_delete=models.PROTECT)
    subtotal = models.BigIntegerField(default=0)
    iva_0 = models.BigIntegerField(default=0)
    iva_5 = models.BigIntegerField(default=0)
    iva_10 = models.BigIntegerField(default=0)
    total = models.BigIntegerField(default=0)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.cliente.nombre
    
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if Company.objects.all().exists():
            self.company = Company.objects.first()
        super(Venta, self).save()


    def toJSON(self):
        item=model_to_dict(self)
        item['ordenVenta']=self.ordenVenta.toJSON()
        item['fecha_venta']=self.fecha_venta.strftime('%Y-%m-%d')
        item['tipo_venta']=self.tipo_venta
        item['fecha_plazo']=self.fecha_plazo.strftime('%Y-%m-%d')
        item['cliente']=self.cliente.toJSON()
        item['subtotal'] = format(self.subtotal)
        item['iva_0'] = format(self.iva_0)
        item['iva_5'] = format(self.iva_5)
        item['iva_10'] = format(self.iva_10)
        item['total'] = format(self.total)
        item['det']=[i.toJSON() for i in self.ventasdet_set.all()]
        return item

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        db_table = 'venta'
        ordering = ['id']

#Ventas detalle
class VentasDet(models.Model):
    venta = models.ForeignKey(Venta,blank=False,null=False,on_delete=models.PROTECT)
    producto = models.ForeignKey(Producto,blank=False,null=False,on_delete=models.PROTECT)
    precio_venta = models.BigIntegerField(default=0)
    cantidad = models.PositiveIntegerField()
    subtotal = models.BigIntegerField(default=0)


    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Venta Det'
        verbose_name_plural = 'Ventas Det'
        db_table = 'venta_det'
        ordering = ['id']
    
    def toJSON(self):
        item=model_to_dict(self,exclude=['ventaa']) 
        item['producto']=self.producto.toJSON()
        item['precio_venta'] = format(self.precio_venta)
        item['subtotal'] = format(self.subtotal)
        return item

#Cuentas por cobrar
class CuentaXcobrar(models.Model):
    venta = models.ForeignKey(Venta,blank=False,null=False,on_delete=models.PROTECT)
    estadoCuenta = (
        ('0', 'Pagado'),
        ('1', 'Deuda'),
    )
    estado = models.CharField(max_length=1, choices=estadoCuenta, default='0') 
    monto_x_cobrar = models.BigIntegerField(default=0)
    saldo = models.BigIntegerField(default=0)

    def __str__(self):
        return str(self.id)

    def toJSON(self):
        item=model_to_dict(self)
        item['venta']=self.venta.toJSON()
        item['estado']=self.estado
        item['monto_x_cobrar'] = format(self.monto_x_cobrar)
        item['saldo'] = format(self.saldo)
        return item

    class Meta:
        verbose_name = 'Cuenta por cobrar'
        verbose_name_plural = 'Cuentas por cobrar'
        db_table = 'cuenta_x_cobrar'
        ordering = ['id']

#cobro
class Cobro(models.Model):
    cuenta_x_cobrar = models.ForeignKey(CuentaXcobrar,blank=False,null=False,on_delete=models.PROTECT)
    fecha_cobro = models.DateField(default=datetime.now, verbose_name="Fecha cobrar")
    monto_cobrado = models.BigIntegerField(default=0)
    caja = models.ForeignKey(Caja,blank=False,null=False,on_delete=models.PROTECT,default='1')
    forma_cobro = models.ForeignKey(FormaPago,blank=False,null=False,on_delete=models.PROTECT,default='1')
    efectivo = models.BigIntegerField(default=0)
    vuelto = models.BigIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    

    def __str__(self):
        return str(self.id)

    def toJSON(self):
        item=model_to_dict(self)
        item['cuenta_x_cobrar']=self.cuenta_x_cobrar.toJSON()
        item['caja']=self.caja.toJSON()
        item['forma_cobro']=self.forma_cobro.toJSON()
        item['user']=self.user.toJSON()
        item['fecha_cobro']=self.fecha_cobro.strftime('%Y-%m-%d')
        item['monto_cobrado'] = format(self.monto_cobrado)
        item['efectivo'] = format(self.efectivo)
        item['vuelto'] = format(self.vuelto)
        return item
    class Meta:
        verbose_name = 'Cobro'
        verbose_name_plural = 'Cuentas cobradas'
        db_table = 'cobro'
        ordering = ['id']

