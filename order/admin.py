from django.contrib import admin
from .models import Order,OrderItem
# Register your models here.
class OrderItemInline(admin.TabularInline):
    model=OrderItem
    raw_id_fields = ('product',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'update_at', 'is_paid')
    readonly_fields=('total', )
    list_filter = ('is_paid',)
    inlines = (OrderItemInline,) 