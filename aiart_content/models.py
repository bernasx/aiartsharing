from django.db import models
from aiart_auth.models import CustomUser
from django.utils import timezone
import uuid

# Create your models here.
class Post(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, default='title')
    publish_date = models.DateTimeField(default=timezone.now)
    views = models.IntegerField(default=0)
