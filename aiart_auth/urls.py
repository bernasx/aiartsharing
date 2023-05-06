from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView

app_name = "auth"
urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name="register"),
    path('profile/<uuid:uuid>', views.ProfileView.as_view(), name="profile"),
    path('profile/', views.ProfileView.as_view(), name="profile"),
    path('profile/edit/',views.ProfileEditView.as_view(), name="profile_edit"),
    path('profile/password/', views.PasswordChange.as_view(), name='password_change')
] 

htmxpatterns = [
   path('follow',views.follow,name="follow"),
]

urlpatterns += htmxpatterns