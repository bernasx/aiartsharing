from django.contrib import admin
from .models import Post
from .forms import PostCreationForm, PostChangeForm
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    add_form = PostCreationForm
    form = PostChangeForm
    model = Post
    fieldsets=[
        (None,{'fields':('title','user','publish_date')})
        ]
    list_display = ('title', 'user', 'publish_date')

admin.site.register(Post, PostAdmin)