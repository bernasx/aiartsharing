from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import RegisterForm


# Create your views here.

class Login(LoginView):
    template_name = 'login.html'
    next_page = reverse_lazy('main:index')

class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()  # save the user
        return super().form_valid(form)
    