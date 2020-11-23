from django.contrib import admin
from .models import (Product, Shopping)
from django.utils.html import format_html

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','cant', 'price', 'pricebs','visible','image_tag')
    readonly_fields = ('image_tag',)
    list_filter = ('name', 'price', 'pricebs')
    search_fields = ('name', 'price', 'pricebs')



class Model1Admin(admin.ModelAdmin):
    list_display = ('codigo_compra','create_at',)


class Model2Admin(admin.ModelAdmin):
    filter_horizontal = ('product',)

admin.site.register(Product,ProductAdmin)
admin.site.register(Shopping,Model2Admin)
