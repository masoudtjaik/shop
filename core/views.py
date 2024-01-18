from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, RedirectView, ListView, DetailView, FormView, CreateView, DeleteView, \
    UpdateView
from django.views.generic.list import ListView


# Create your views here.


class Home(View):
    template = 'core/home.html'

    def get(self, request):
        return render(request, self.template)
