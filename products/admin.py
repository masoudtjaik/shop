from django.contrib import admin
from .models import Product, Discount, Like, Comment, Category, Image

# Register your models here.

admin.site.register((Discount,  Category, Image))


@admin.register(Product)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'inventory', 'price')
    search_fields = ('name',)
    readonly_fields = ('price_discount',)


@admin.register(Like)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')


@admin.register(Comment)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')
