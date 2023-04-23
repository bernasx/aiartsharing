from django.urls import path
from . import views

app_name = 'content'
urlpatterns = [
   path('create/',views.CreateImagePostView, name='create_imagepost'),
   path('detail/<uuid:uuid>', views.DetailImagePostView.as_view(), name='detail_imagepost'),
   path('posts/',views.ListImagePostsView.as_view(), name='list_imagepost')
]