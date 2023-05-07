from django.db import models
from aiart_auth.models import CustomUser
from aiart_content.models import ImagePost
from django.utils import timezone
import uuid
# Create your models here.


class Report(models.Model):

    report_choices = [
    ("report_broken_url", "I can't view the image for this post."),
    ("report_not_aiart", "This post is not AI Art."),
    ("report_harassment", "This post is targetted harassment."),
    ("report_selfharm", "This post is promoting suicide or self-harm."),
    ("report_spam", "This post is spam."),
    ("report_untagged_sexual_content", "This post is not tagged for sexual content (18+)."),
    ("report_sexual_content_minors", "This post contains sexual content involving minors."),
    ("report_other", "Other (please use the box below)"),
    ]

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
    report_date = models.DateTimeField(default=timezone.now, editable=False)
    report_option = models.CharField(max_length=300, choices=report_choices)
    other_option = models.TextField()

class ImagePostReport(Report):
    imagepost = models.ForeignKey(ImagePost, on_delete=models.CASCADE, editable=False)