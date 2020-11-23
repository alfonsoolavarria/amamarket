from django.db import models
from django.utils.safestring import mark_safe
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver


# Create your models here.

class Product(models.Model):
    # __cate=((1,_('Viveres')),(2,_('Frigorifico')),(3,_('Enlatados')),(4,_('Charcuteria')),(5,_('Carnes')),(6,_('Personales')),(7,_('Chucherias')))
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=1000,help_text="Alias de la imagen")
    price=models.DecimalField(max_digits=30, decimal_places=2,help_text="Precio en Dolares")
    pricebs=models.DecimalField(max_digits=30, decimal_places=2,default=1,help_text="Precion en Bolivares")
    description=models.CharField(max_length=200,help_text="Descripcion del producto")
    name_image=models.CharField(max_length=50,help_text="Debes colocar el nombre de la imagen con la extension por ejemplo: imagen.png ")
    picture = models.ImageField(upload_to='imagesp')
    cant=models.PositiveSmallIntegerField(default=1,help_text="Cantidad disponible el producto en el almacen")
    # category=models.PositiveSmallIntegerField(choices=__cate,help_text="Seleccione una categoria del producto")
    visible = models.BooleanField(default=False)
    create_at=models.DateTimeField(auto_now_add=True,null=True)
    def image_tag(self):
        return mark_safe('<img src="/static/images/upload/%s" style="width: 45px; height:45px;" />' % self.picture.name)
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Productos"




class Shopping(models.Model):#compra
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=1000,help_text="Nombre")
    product=models.ManyToManyField(Product, related_name='seleccion_products')
    cantidad=models.CharField(default=0,max_length=500,help_text="cantidad por producto separado por coma")
    monto=models.CharField(max_length=1000,help_text="Precio de la venta en $")
    create_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Compras"

@receiver(m2m_changed, sender=Shopping.product.through)
def update_stock(sender, instance, **kwargs):
    import ast
    action = kwargs.pop('action', None)
    action = action.split('_')
    if action[0] == 'post':
        if isinstance(instance.cantidad,int):
            cantidades = instance.cantidad
        else:
            cantidades = ast.literal_eval(instance.cantidad)
        for index,value in enumerate(instance.product.all()):
            c = Product.objects.get(id=value.id)
            if isinstance(cantidades,int):
                c.cant = c.cant - cantidades
            elif isinstance(cantidades,tuple):
                c.cant = c.cant - cantidades[index]
            else:
                pass
            c.save()
