from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic.edit import FormView, UpdateView
from django.contrib.auth import logout
from django.views.generic import DetailView
from django.urls import reverse_lazy
from .forms import RegisterForm, LoginForm, EditProfileForm
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.

class Login(LoginView):
    template_name = 'login.html'
    next_page = reverse_lazy('main:index')
    authentication_form = LoginForm

class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('auth:login')

    def form_valid(self, form):
        form.save()  # save the user
        return super().form_valid(form)


class ProfileView(DetailView):
    model = CustomUser
    template_name = 'profile/profile.html'

    
    def get_object(self):
        if not self.kwargs.get('uuid'):
            return CustomUser.objects.get(pk=self.request.user.pk)
        return CustomUser.objects.get(uuid=self.kwargs.get('uuid'))
    
@method_decorator(login_required, name='dispatch')
class ProfileEditView(UpdateView):
    model = CustomUser
    template_name = 'profile/edit.html'
    form_class = EditProfileForm
    success_url = reverse_lazy('auth:profile')

    def get_object(self):
        return CustomUser.objects.get(pk=self.request.user.pk)
    
@method_decorator(login_required, name='dispatch')
class PasswordChange(PasswordChangeView):
    model = CustomUser
    template_name = 'profile/password.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('auth:login')

    def form_valid(self, form):
        form.save()
        self.request.session.flush()
        logout(self.request)
        return super().form_valid(form)