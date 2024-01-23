from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django import forms


class CustomUserCreationForm(UserCreationForm):
    # password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    # password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [ 'email', 'username', 'phone_number', 'gender', 'birthday', 'password1',
                  'password2']
        # labels = {
        #     'first_name': 'نام',
        #     'last_name': 'نام خانوادگی',
        #     'email': 'ایمیل',
        #     'phone_number': 'شماره تلفن',
        #     'birthday': 'تاریخ تولد',
        #     'city': 'شهر',
        #     'address': 'آدرس',
        #     'gender': 'جنسیت',
        #     'image': 'تصویر',
        # }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'phone_number')


class MyLoginForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"placeholder": "Phone or Email"}))
    password = forms.CharField(widget=forms.PasswordInput())


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = [ 'email', 'username', 'phone_number', 'password1', 'password2']


class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)

# class LoginForm(forms.Form):
#     username = forms.CharField(max_length=50)
#     password = forms.CharField(max_length=50, widget=forms.PasswordInput)
