from django.urls import path
from . import views

app_name = 'content'
urlpatterns = [
   path('create/',views.CreateImagePostView, name='create_imagepost'),
   path('detail/<uuid:uuid>', views.DetailImagePostView.as_view(), name='detail_imagepost'),
   path('posts/',views.ListImagePostsView.as_view(), name='list_imagepost'),
   path('followingfeed/',views.ListImagePostsFollowingFeed.as_view(), name='following_feed'),
   path('favorites/',views.ListImagePostsFavorites.as_view(), name='favorites')
]

htmx_urlpatterns = [
   path('like_imagepost/', views.likeImagePost, name="like_imagepost"),
   path('favorite_imagepost/', views.favoriteImagePost, name="favorite_imagepost"),
   path('search/',views.searchView, name='search'),
   path('post_comment',views.postComment,name="post_comment")
]


urlpatterns += htmx_urlpatterns