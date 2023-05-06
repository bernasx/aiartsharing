from django.contrib import admin
from .models import ImagePost
from .forms import ImagePostCreationForm, ImagePostChangeForm
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    add_form = ImagePostCreationForm
    form = ImagePostChangeForm
    model = ImagePost
   
    readonly_fields=('user','publish_date')
    list_display = ('user', 'publish_date')

admin.site.register(ImagePost, PostAdmin)