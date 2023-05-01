from django.shortcuts import render
from aiart_content.forms import SimpleSearchForm, AdvancedLocalSearchForm, AdvancedOnlineServiceSearchForm
from aiart_content.models import ImagePost
# Create your views here.

def index(request):
    simpleform = SimpleSearchForm
    advanced_local_form = AdvancedLocalSearchForm
    advanced_online_form = AdvancedOnlineServiceSearchForm
    totalPosts = ImagePost.objects.count()
    context = {'simpleform':simpleform, 'advanced_local_form':advanced_local_form, 'advanced_online_form': advanced_online_form, 'totalPosts':totalPosts}
    return render(request, template_name='index.html', context=context)

def about(request):
    return render(request, template_name='about.html')

def help(request):
    return render(request, template_name='help.html')

def contact(request):
    return render(request, template_name='contact.html')