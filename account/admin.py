from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm


# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = User
    form = CustomUserChangeForm
    list_display = ['username','user_type', 'email', 'birthday', 'phone_number']
    fieldsets = UserAdmin.fieldsets + (
        ('Others', {'fields': ('user_type','birthday', 'phone_number', 'image')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'birthday', 'phone_number', 'image','user_type')}),
    )


admin.site.register(User, CustomUserAdmin)
