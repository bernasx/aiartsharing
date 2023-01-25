from django.db import models
from aiart_auth.models import CustomUser
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=128, default='title')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    publish_date = models.DateTimeField(default=timezone.now)