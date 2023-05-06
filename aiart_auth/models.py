from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import CustomUserManager
from django.utils import timezone
import os
import uuid

# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    username = models.CharField(max_length=24)
    profile_picture = models.ImageField(upload_to='media/pfp/', default='media/pfp/default.png', blank=True)
    profile_picture_last_update = models.DateTimeField(default=timezone.now)
    bio = models.TextField(max_length=250, default="")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    # Likes and Favorites
    liked_image_posts = models.ManyToManyField('aiart_content.ImagePost', related_name='liked_image_posts')
    favorited_image_posts = models.ManyToManyField('aiart_content.ImagePost', related_name='favorited_image_posts')

    def __str__(self):
        return self.email

    def profilePictureFilename(self):
        return os.path.basename(self.profile_picture.name)