from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django import forms
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    # password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    # password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['user_type' ,'email', 'username', 'phone_number', 'gender', 'birthday', 'password1',
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
        fields = ('email', 'username', 'phone_number',)


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

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'phone_number', 'image', 'gender', 'birthday')


class PasswordForm(forms.Form):
    password_before = forms.CharField(label="Your password", required=True
                                      , widget=forms.PasswordInput())
    password_new = forms.CharField(label="New password", required=True
                                   , widget=forms.PasswordInput())
    password_again = forms.CharField(label="Confirm password", required=True
                                     , widget=forms.PasswordInput())

    # def clean_password_before(self):
    #     password = self.cleaned_data.get('password_before')
    #     if self.request.user.check_password(password):
    #         raise ValidationError(" password is wrong")
    #     return password

    def clean(self):
        result = super().clean()
        password1 = result.get('password_new')
        password2 = result.get('password_again')
        if password1 and password1 and password1 != password2:
            raise ValidationError("password must be match")
        return result
