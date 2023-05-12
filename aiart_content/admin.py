from django.contrib import admin
from .models import ImagePost
from .forms import ImagePostChangeForm
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    add_form = ImagePostChangeForm
    form = ImagePostChangeForm
    model = ImagePost
   
    readonly_fields=('user','publish_date','model','hypernetwork','positive_prompt','negative_prompt','notes','generation_details','image_url','onlineService')
    list_display = ('user', 'publish_date')

admin.site.register(ImagePost, PostAdmin)