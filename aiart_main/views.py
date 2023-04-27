from django.shortcuts import render
from aiart_content.forms import SimpleSearchForm
# Create your views here.

def index(request):
    form = SimpleSearchForm
    context = {'form':form}
    return render(request, template_name='index.html', context=context)