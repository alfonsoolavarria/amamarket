from django.contrib import admin
from .models import (Product, Shopping)
from django.utils.html import format_html
from django import forms
from django.contrib.admin import SimpleListFilter

# Register your models here.

# make_published.short_description = "Mark selected stories as published"

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','cant', 'price', 'pricebs','visible','image_tag')
    readonly_fields = ('image_tag',)
    list_filter = ('name', 'price', 'pricebs')
    search_fields = ('name', 'price', 'pricebs')

from django import forms

class EquipmentModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.fields['product'].queryset = Product.avail.all()


class Model2Admin(admin.ModelAdmin):
    form = EquipmentModelForm
    filter_horizontal = ['product',]
    readonly_fields = ('monto',)


admin.site.register(Product,ProductAdmin)
admin.site.register(Shopping,Model2Admin)
