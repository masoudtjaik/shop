from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, RedirectView, ListView, DetailView, FormView, CreateView, DeleteView, \
    UpdateView
from django.contrib.auth import login, authenticate, logout
from .forms import MyLoginForm, UserCreateForm
from .models import User
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q


class Login(View):
    template_class = "account/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("core:home")
        else:
            return super().dispatch(request, *args, **kwargs)

    def setup(self, request, *args, **kwargs) -> None:
        self.next = request.GET.get("next")
        request.session["next"] = self.next
        return super().setup(request, *args, **kwargs)

    def get(self, request):
        print(request.session.get('username'))
        return render(request, self.template_class)

    # def post(self, request):
    #     if request.POST.get("email"):
    #         if request.POST.get("pass"):
    #             email = request.POST.get("email")
    #             password = request.POST.get("pass")
    #             user = authenticate(username=email, password=password)
    #             if user:
    #                 login(request, user)
    #                 if self.next:
    #                     return redirect(self.next)
    #                 return redirect("core:home")
    #             else:
    #                 messages.success(request, 'User Or Password is Wrong ', 'danger')
    #                 return render(request, self.template_class)
    #         else:
    #             messages.success(request, 'field password Is Empty ', 'danger')
    #             return render(request, self.template_class)
    #     else:
    #         messages.success(request, 'field email or phone Is Empty ', 'danger')
    #         return render(request, self.template_class)
    def post(self, request):
        if request.POST.get("email"):
            email = request.POST.get("email")
            user = User.objects.filter(Q(username=email) | Q(phone_number=email)).exists()
            email = User.objects.filter(email=email).exists()
            if user:
                request.session["username"] = request.POST.get("email")
                return redirect("account:password")
            elif email:
                send_mail(
                    'subject',
                    'hello masoud',
                    'setting.EMAIL_HOST_USER',
                    [request.POST.get("email")],
                    fail_silently=False
                )
                return redirect("account:confirm_email")
            else:
                messages.success(request, 'username or phone number not found ', 'danger')
                return render(request, self.template_class)
        else:
            messages.success(request, 'field email or phone Is Empty ', 'danger')
            return render(request, self.template_class)


class Password(Login):
    template_class = "account/password.html"

    def post(self, request):
        print('hello')
        if request.POST.get("pass"):
            email = request.session.get("username")
            password = request.POST.get("pass")
            user = authenticate(username=email, password=password)
            if user:
                login(request, user)
                if self.next:
                    return redirect(self.next)
                return redirect("core:home")
            else:
                messages.success(request, 'Password is Wrong ', 'danger')
                return render(request, self.template_class)
        else:
            messages.success(request, 'field Password Is Empty ', 'danger')
            return render(request, self.template_class)


class Logout(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect("core:home")


class SingUp(CreateView):
    template_name = 'account/signup.html'
    # model = User
    form_class = UserCreateForm
    # fields = ['email', 'username', 'phone_number', 'password', 'password2']
    success_url = reverse_lazy('core:home')


class Signup2(View):
    url = 'account/signup.html'

    def get(self, request):
        form = UserCreateForm()
        return render(request, self.url, {'form': form})

    def post(self, request):
        form = UserCreateForm(request.POST)
        if form.is_valid():
            # form.save()
            email = form.cleaned_data['email']
            send_mail(
                'subject',
                'hello masoud',
                'setting.EMAIL_HOST_USER',
                [email],
                fail_silently=False
            )
            return redirect('account:code')
        return render(request, self.url, {'form': form})


class ConfirmEmail(View):
    url = 'account/confirm_email.html'

    def get(self, request):
        return render(request, self.url)

    def post(self, request):
        # form = UserCreateForm(request.POST)
        # if form.is_valid():
        #     print('hello')
        #     form.save()
        #     return redirect('core:home')
        return render(request, self.url)
