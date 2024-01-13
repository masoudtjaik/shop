from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'birthday', 'phone_number']
    fieldsets = UserAdmin.fieldsets + (
        ('Others', {'fields': ('birthday','phone_number','image')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('birthday','phone_number','image')}),
    )


admin.site.register(User, CustomUserAdmin)