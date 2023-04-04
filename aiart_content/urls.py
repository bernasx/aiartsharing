from django.urls import path

from . import views

urlpatterns = [
   path('create/',views.CreateImagePostView.as_view(), name='create_imagepost'),
   path('detail/<uuid:uuid>', views.DetailImagePostView.as_view(), name='detail_imagepost'),
   path('posts/',views.ListImagePostsView.as_view(), name='list_imagepost')
]