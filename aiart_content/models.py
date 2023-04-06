from django.db import models
from aiart_auth.models import CustomUser
from django.utils import timezone
import uuid

# Create your models here.
class Post(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    publish_date = models.DateTimeField(default=timezone.now, editable=False)

class ImagePost(Post):
    # Model Constants
    DALL_E = 'DALLE'
    NOVEL_AI = 'NAI'
    MIDJOURNEY = 'MJ'

    ONLINE_SERVICES = [(DALL_E,'DALL-E 2'),(NOVEL_AI,'Novel AI'),(MIDJOURNEY,'Midjourney')]


    # Stable Diffusion Type of Generation
    image_url = models.URLField(max_length=256)
    model = models.CharField(max_length=256)
    hypernetwork = models.CharField(max_length=256, blank=True)
    positive_prompt = models.TextField()
    negative_prompt = models.TextField(blank=True)
    notes = models.TextField()
    generation_details = models.CharField(max_length=300, blank=True)

    # Online Services
    isOnlineService = models.BooleanField(default=False)
    onlineService = models.CharField(max_length=256, choices=ONLINE_SERVICES, blank=True)