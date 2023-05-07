from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic.edit import FormView, UpdateView
from django.contrib.auth import logout
from django.views.generic import DetailView
from django.urls import reverse_lazy
from .forms import RegisterForm, LoginForm, EditProfileForm
from .models import *
from aiart_content.models import ImagePost
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Count
from django.shortcuts import render
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            user = CustomUser.objects.get(uuid=self.kwargs.get('uuid'))
        except(CustomUser.DoesNotExist):
            user = CustomUser.objects.get(pk=self.request.user.pk)

        post_count = ImagePost.objects.filter(user=user).count()
        #not entirely sure how this works but it returns the total_likes of all posts of a given user
        total_likes = ImagePost.objects.filter(user=user).aggregate(Count('liked_image_posts'))['liked_image_posts__count']
        user_posts = ImagePost.objects.filter(user=user).order_by('-publish_date')[:18]
        context['user_posts'] = user_posts
        context['post_count'] = post_count
        context['total_likes'] = total_likes
        context['user_being_followed'] = user.uuid

        if(Followers.objects.filter(user_being_followed=user,user_following=self.request.user).exists()):
            context['following_user'] = True
        else:
            context['following_user'] = False

        return context

    
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
    

#HTMX Views

def follow(request):
    # the one being followed
    user = CustomUser.objects.get(uuid=request.POST.get('user_followed'))

    if(user == request.user):
        return

    if(Followers.objects.filter(user_being_followed=user,user_following=request.user).exists()):
        Followers.objects.get(user_being_followed=user,user_following=request.user).delete()
        context = {'following_user':False,'user_being_followed':user.uuid}
        return render(request, 'profile/partials/follow.html', context=context)
    else:
        follow = Followers.objects.create(user_being_followed=user,user_following=request.user)
        follow.save()
        context = {'following_user':True,'user_being_followed':user.uuid}
        return render(request, 'profile/partials/follow.html', context=context)