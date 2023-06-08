from django.views.generic import DetailView, ListView
from .forms import ImagePostLocalCreationForm, ImagePostOnlineCreationForm, SimpleSearchForm, AdvancedLocalSearchForm, AdvancedOnlineServiceSearchForm, CommentCreationForm
from aiart_main.forms import ImagePostReportForm
from .models import ImagePost, ImagePostComment
from django.shortcuts import render, redirect, HttpResponse
from aiart_auth.models import CustomUser, Followers
from django.urls import reverse
from django.db.models import Q
from django.db.models import Count
# Create your views here.

def CreateImagePostView(request):
    if(request.method == 'GET'):
        local_form = ImagePostLocalCreationForm
        online_form = ImagePostOnlineCreationForm
        context = {'local_form':local_form, 'online_form':online_form}
        return render(request,'imageposts/create.html', context)
    if(request.method =='POST'):
        context = {}
        if(request.POST['post_type'] == 'local'):
            local_form = ImagePostLocalCreationForm(request.POST, request.FILES)
            online_form = ImagePostOnlineCreationForm
            context = {'local_form':local_form, 'online_form':online_form}
            if local_form.is_valid():
                imagepost = ImagePost(
                    user = request.user,
                    image_url = request.POST['image_url'],
                    positive_prompt = request.POST['positive_prompt'],
                    notes = request.POST['notes'],
                    generation_details = request.POST['generation_details'],
                    model = request.POST['model'],
                    hypernetwork = request.POST['hypernetwork'],
                    negative_prompt = request.POST['negative_prompt'],
                    isOnlineService = False,
                )
                imagepost.save()
                return redirect('content:detail_imagepost',uuid=imagepost.uuid)
            else:
                context['onlineServiceReload'] = False
                return render(request,'imageposts/create.html', context)
        else: 
            local_form = ImagePostLocalCreationForm
            online_form = ImagePostOnlineCreationForm(request.POST, request.FILES)
            context = {'local_form':local_form, 'online_form':online_form}
            if online_form.is_valid():
                imagepost = ImagePost (
                    user = request.user,
                    image_url = request.POST['image_url'],
                    positive_prompt = request.POST['positive_prompt'],
                    notes = request.POST['notes'],
                    generation_details = request.POST['generation_details'],
                    negative_prompt = request.POST['negative_prompt'],
                    onlineService = request.POST['onlineService'],
                    isOnlineService = True,
                )

                if request.POST['model'] != '':
                    imagepost.model = request.POST['model']
                else:
                    imagepost.model = imagepost.onlineService

                imagepost.save()
                return redirect('content:detail_imagepost',uuid=imagepost.uuid)
            else:
                context['onlineServiceReload'] = True
                return render(request,'imageposts/create.html', context)


class DetailImagePostView(DetailView):
    model = ImagePost
    template_name = 'imageposts/detail.html'


    def get_object(self):
        post = ImagePost.objects.get(uuid=self.kwargs.get('uuid'))
        post.views += 1
        post.save()
        return post
    
    def get_context_data(self, **kwargs):
         # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        post = ImagePost.objects.get(uuid=self.kwargs.get('uuid'))
        # We have to separate these from the rest of the page so HTMX can rewrite them and preserve stuff in the template
        context['imagepost_uuid'] = post.uuid
        if self.request.user.is_authenticated:
            context['user_liking_uuid'] = self.request.user.uuid
        context['likes'] = post.liked_image_posts.all().count()
        context['report_form'] = ImagePostReportForm

        # gets random posts to be recommended, this is super slow and should be changed eventually
        recommended_posts = ImagePost.objects.all().exclude(uuid=self.kwargs.get('uuid')).order_by('?')[:6]
        context['recommended_posts'] = recommended_posts

        if self.request.user.is_authenticated:
            #Handling likes and Favorites
            if self.request.user.liked_image_posts.filter(uuid=ImagePost.objects.get(uuid=self.kwargs.get('uuid')).uuid).exists():
                # These have to be strings because that's how we get them from the client. Could make them bools but it's just one comparison when rendering the template
                # so it's probably fine.
                context['user_liked_post'] = "True" 


            if self.request.user.favorited_image_posts.filter(uuid=ImagePost.objects.get(uuid=self.kwargs.get('uuid')).uuid).exists():
                context['user_favorited_post'] = "True"

        #comment section
        context['comments'] = ImagePostComment.objects.filter(imagepost=post).order_by('-publish_date')
        form = CommentCreationForm
        context['comment_form'] = form
        return context
    
class ListImagePostsView(ListView):
    model = ImagePost
    template_name = 'imageposts/posts.html'
    paginate_by = 24 

    def get_queryset(self):

        try: 

            # order the posts by whatever
            ordering = ''
            order_query = self.request.GET['sort_by']

            if(order_query == 'recent'):
                ordering = '-publish_date'
            elif(order_query == 'popular'):
                ordering = '-likes'
            elif(order_query == 'views'):
                ordering = '-views'
            else:
                ordering = '-recent'

            # get each a query from each form or type of search individually    
            if (self.request.GET['search_type'] == 'simple'):
                
                keyword = self.request.GET['keyword']
                return ImagePost.objects.filter(
                    Q(positive_prompt__icontains=keyword) | 
                    Q(generation_details__icontains=keyword) | 
                    Q(notes__icontains=keyword) | 
                    Q(model__icontains=keyword)).annotate(likes=Count('liked_image_posts')).order_by(ordering)
            
            elif (self.request.GET['search_type'] == 'advanced_local'):
                prompt = self.request.GET['prompt']
                model = self.request.GET['model']
                keyword = self.request.GET['keyword']
                return ImagePost.objects.filter(Q(isOnlineService=False) & 
                                                Q(positive_prompt__icontains=prompt) & 
                                                Q(model__icontains=model) & 
                                                (Q(generation_details__icontains=keyword) |Q(notes=keyword))).annotate(likes=Count('liked_image_posts')).order_by(ordering)
            
            
            elif (self.request.GET['search_type'] == 'advanced_online'):
                
                prompt = self.request.GET['prompt']
                service = self.request.GET['service']
                keyword = self.request.GET['keyword']
                return ImagePost.objects.filter(Q(isOnlineService=True) 
                                                & Q(positive_prompt__icontains=prompt) 
                                                & Q(onlineService__icontains=service) 
                                                & Q(notes__icontains=keyword)).annotate(likes=Count('liked_image_posts')).order_by(ordering)
            
            
            elif (self.request.GET['search_type'] == 'by_user'):
                
                useruuid = self.request.GET['user_searched']
                user = CustomUser.objects.get(uuid=useruuid)
                return ImagePost.objects.filter(user=user).annotate(likes=Count('liked_image_posts')).order_by(ordering)
            
            else:
                
                return ImagePost.objects.all().annotate(likes=Count('liked_image_posts')).order_by(ordering)
            
        except (KeyError):
        
            return ImagePost.objects.all().annotate(likes=Count('liked_image_posts')).order_by('-publish_date')
        
    def get_context_data(self, **kwargs):
    
        context = super().get_context_data(**kwargs)
        simpleform = SimpleSearchForm
        advanced_local_form = AdvancedLocalSearchForm
        advanced_online_form = AdvancedOnlineServiceSearchForm
        context['simpleform'] = simpleform
        context['advanced_local_form'] = advanced_local_form
        context['advanced_online_form'] = advanced_online_form

        #preserve search parameters, if any
        get_copy = self.request.GET.copy()
        parameters = get_copy.pop('page', True) and get_copy.urlencode()
        context['parameters'] = parameters
        return context

class ListImagePostsFollowingFeed(ListView):
    model = ImagePost
    template_name = 'imageposts/following_feed.html'
    paginate_by = 24 

    def get_queryset(self):
        following_objects = Followers.objects.filter(user_following=self.request.user)
        users = map(lambda x: x.user_being_followed, following_objects)
        return ImagePost.objects.filter(user__in=users).annotate(likes=Count('liked_image_posts')).order_by('-publish_date')
    
    def get_context_data(self, **kwargs):
    
        context = super().get_context_data(**kwargs)

        #preserve search parameters, if any
        get_copy = self.request.GET.copy()
        parameters = get_copy.pop('page', True) and get_copy.urlencode()
        context['parameters'] = parameters
        return context
    
class ListImagePostsFavorites(ListView):
    model = ImagePost
    template_name = 'imageposts/favorites.html'
    paginate_by = 24 

    def get_queryset(self):
        user = self.request.user
        return user.favorited_image_posts.annotate(likes=Count('liked_image_posts')).order_by('-publish_date')
    
    def get_context_data(self, **kwargs):
    
        context = super().get_context_data(**kwargs)

        #preserve search parameters, if any
        get_copy = self.request.GET.copy()
        parameters = get_copy.pop('page', True) and get_copy.urlencode()
        context['parameters'] = parameters
        return context

def searchView(request):
    qdict = request.POST.copy()
    try:
        qdict.pop('csrfmiddlewaretoken')
    except(KeyError):
        return HttpResponse('Key error on csrfmiddleware')
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

def postComment(request):
    if(request.method =='POST'):
        post = ImagePost.objects.get(uuid=request.POST.get('post_uuid'))
        user = CustomUser.objects.get(uuid=request.POST.get('user_commenting'))
        content = request.POST.get('content')
        comment = ImagePostComment(user=user,imagepost=post,content=content)
        comment.save()
        comments = ImagePostComment.objects.filter(imagepost=post).order_by('-publish_date')
        context = {'comments':comments, 'post_uuid':post.uuid,'user_commenting':user.uuid}
        return render(request, 'comments/commentlist.html', context=context)
