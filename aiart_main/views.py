from django.shortcuts import render
from aiart_content.forms import SimpleSearchForm, AdvancedLocalSearchForm, AdvancedOnlineServiceSearchForm
# Create your views here.

def index(request):
    simpleform = SimpleSearchForm
    advanced_local_form = AdvancedLocalSearchForm
    advanced_online_form = AdvancedOnlineServiceSearchForm
    context = {'simpleform':simpleform, 'advanced_local_form':advanced_local_form, 'advanced_online_form': advanced_online_form}
    return render(request, template_name='index.html', context=context)