from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import ImagePostCreationForm
from .models import ImagePost
from django.urls import reverse_lazy
# Create your views here.

class CreateImagePostView(CreateView):
    model = ImagePost
    form_class = ImagePostCreationForm
    template_name = 'imageposts/create.html'
    # TODO - edit this success_url to post itself
    success_url = reverse_lazy('list_imagepost')

class ListImagePostsView(ListView):
    model = ImagePost
    template_name = 'imageposts/posts.html'

class DetailImagePostView(DetailView):
    model = ImagePost
    template_name = 'imageposts/detail.html'

    def get_object(self):
        return ImagePost.objects.get(uuid=self.kwargs.get('uuid'))
