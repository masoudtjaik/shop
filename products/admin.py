from django.contrib import admin
from .models import Product,Discount,Like,Comment,Category
# Register your models here.

admin.site.register((Product,Discount,Like,Comment,Category))