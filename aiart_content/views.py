from django.views.generic import DetailView, ListView
from django.contrib.auth.decorators import login_required
from .forms import ImagePostCreationForm, SimpleSearchForm
from .models import ImagePost
from django.shortcuts import render, redirect
from aiart_auth.models import CustomUser
from django.urls import reverse
from django.db.models import Q

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


class DetailImagePostView(DetailView):
    model = ImagePost
    template_name = 'imageposts/detail.html'
    def get_object(self):
        return ImagePost.objects.get(uuid=self.kwargs.get('uuid'))
    
    def get_context_data(self, **kwargs):
         # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # We have to separate these from the rest of the page so HTMX can rewrite them and preserve stuff in the template
        context['imagepost_uuid'] = self.kwargs.get('uuid')
        context['user_liking_uuid'] = self.request.user.uuid

        if self.request.user.liked_image_posts.filter(uuid=ImagePost.objects.get(uuid=self.kwargs.get('uuid')).uuid).exists():
            # These have to be strings because that's how we get them from the client. Could make them bools but it's just one comparison when rendering the template
            # so it's probably fine.
            context['user_liked_post'] = "True" 


        if self.request.user.favorited_image_posts.filter(uuid=ImagePost.objects.get(uuid=self.kwargs.get('uuid')).uuid).exists():
            context['user_favorited_post'] = "True"

        return context
    
class ListImagePostsView(ListView):
    model = ImagePost
    template_name = 'imageposts/posts.html'
    paginate_by = 24 

    def get_queryset(self):
        try: 
            if (self.request.GET['search_type'] == 'simple'):
                keyword = self.request.GET['keyword']
                return ImagePost.objects.filter(Q(positive_prompt__icontains=keyword) | Q(generation_details__icontains=keyword) | Q(notes__icontains=keyword) | Q(model__icontains=keyword) ).order_by('-publish_date')
            elif (self.request.GET['search_type'] == 'advanced_local'):
                prompt = self.request.GET['prompt']
                model = self.request.GET['model']
                keyword = self.request.GET['keyword']

                return ImagePost.objects.filter(Q(isOnlineService=False) & Q(positive_prompt__icontains=prompt) & Q(model__icontains=model) & (Q(generation_details__icontains=keyword) |Q(notes=keyword))).order_by('-publish_date')
            elif (self.request.GET['search_type'] == 'advanced_online'):
                prompt = self.request.GET['prompt']
                service = self.request.GET['service']
                print(service)
                keyword = self.request.GET['keyword']
                return ImagePost.objects.filter(Q(isOnlineService=True) & Q(positive_prompt__icontains=prompt) & Q(onlineService__icontains=service) & Q(notes__icontains=keyword)).order_by('-publish_date')
            else:
                return ImagePost.objects.all().order_by('-publish_date')
        except (KeyError):
       
            return ImagePost.objects.all().order_by('-publish_date')   
    

def searchView(request):
    qdict = request.POST.copy()
    qdict.pop('csrfmiddlewaretoken')
    return redirect(reverse('content:list_imagepost') + '?' + qdict.urlencode())
    

# HTMX Views

def likeImagePost(request):
    liked_post = ImagePost.objects.get(uuid=request.POST.get('liked_post'))
    user = CustomUser.objects.get(uuid=request.POST.get('user_liking'))
    user_liked_post = "True"
    user_did_favorite_post = request.POST.get('user_did_favorite_post') # Need this to keep track of client side icons for like/favorite.... yeah... it ain't great but whatever

    if user.liked_image_posts.filter(uuid=liked_post.uuid).exists():
        user.liked_image_posts.remove(user.liked_image_posts.get(uuid=liked_post.uuid))
        user_liked_post = "False"
    else:
        user.liked_image_posts.add(liked_post)
    
    context = {'imagepost_uuid':liked_post.uuid,'user_liking_uuid':user.uuid,'user_liked_post':user_liked_post, 'user_favorited_post':user_did_favorite_post}
    return render(request, 'imageposts/partials/detail_like_favorite_buttons.html', context=context)

def favoriteImagePost(request):
    # we can reuse the attributes from the other POST request, no need to change names I guess
    liked_post = ImagePost.objects.get(uuid=request.POST.get('liked_post'))
    user = CustomUser.objects.get(uuid=request.POST.get('user_liking'))
    user_favorited_post = "True"
    user_did_like_post = request.POST.get('user_did_like_post') 

    if user.favorited_image_posts.filter(uuid=liked_post.uuid).exists():
        user.favorited_image_posts.remove(user.favorited_image_posts.get(uuid=liked_post.uuid))
        user_favorited_post = "False"
    else:
        user.favorited_image_posts.add(liked_post)
    
    context = {'imagepost_uuid':liked_post.uuid,'user_liking_uuid':user.uuid,'user_favorited_post':user_favorited_post, 'user_liked_post':user_did_like_post}

    return render(request, 'imageposts/partials/detail_like_favorite_buttons.html', context=context)

