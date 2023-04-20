from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import ImagePostCreationForm
from .models import ImagePost
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.utils import timezone

# Create your views here.

def CreateImagePostView(request):
    if(request.method == 'GET'):
        form = ImagePostCreationForm
        context = {'form':form}
        return render(request,'imageposts/create.html', context)
    if(request.method =='POST'):
        form = ImagePostCreationForm(request.POST, request.FILES)
        context = {'form':form}
        if form.is_valid():
            imagepost = ImagePost(
                user = request.user,
                image_url = request.POST['image_url'],
                positive_prompt = request.POST['positive_prompt'],
                notes = request.POST['notes'],
                generation_details = request.POST['generation_details']
            )
            checks = request.POST.getlist('isOnlineService')
            if('on' in checks):
                # creating an online service image
                imagepost.onlineService = request.POST['onlineService']
                imagepost.isOnlineService = True
                imagepost.model = imagepost.onlineService

            else:
                #creating a normal stable diffusion image post
                imagepost.model = request.POST['model']
                imagepost.hypernetwork = request.POST['hypernetwork']
                imagepost.negative_prompt = request.POST['negative_prompt']

            imagepost.save()
            return redirect('content:detail_imagepost',uuid=imagepost.uuid)
        return render(request,'imageposts/create.html', context)

class ListImagePostsView(ListView):
    model = ImagePost
    template_name = 'imageposts/posts.html'
    paginate_by = 24 
    ordering = ['-publish_date']

class DetailImagePostView(DetailView):
    model = ImagePost
    template_name = 'imageposts/detail.html'
    def get_object(self):
        return ImagePost.objects.get(uuid=self.kwargs.get('uuid'))