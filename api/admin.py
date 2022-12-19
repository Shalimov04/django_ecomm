from django.contrib import admin
from django.utils.safestring import mark_safe
from api.models import *


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    empty_value_display = '-'
    list_display = ('name', 'origin', 'tel')
    list_filter = ['origin']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        kwargs["queryset"] = Category.objects.filter(name__in=['God', 'Demi God'])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    empty_value_display = '-'


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    empty_value_display = '-'
    list_display = ('name', 'email', 'phone')


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    empty_value_display = '-'
    list_display = ('date', 'provider')
    list_filter = ['provider']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    empty_value_display = '-'
    list_display = ('pk', 'category', 'name', 'condition', 'image_show', 'price', 'count')
    list_filter = ('category', 'brand')

    def image_show(self, obj):
        if obj.image:
            return mark_safe('<img src = "{}" width="100" />'.format(obj.image.url))
        return 'None'

    image_show.__name__ = 'Изображение'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    empty_value_display = '-'
    list_display = ('order_date', 'completed', 'completion_date', 'customer')


@admin.register(OrderedItem)
class OrderedItemAdmin(admin.ModelAdmin):
    empty_value_display = '-'
    list_display = ('order', 'count', 'cost', 'item')


@admin.register(PickupAddress)
class PickupAddressAdmin(admin.ModelAdmin):
    list_display = ['details']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'device']
