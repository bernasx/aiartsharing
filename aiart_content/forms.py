from django import forms
from .models import ImagePost


class ImagePostCreationForm(forms.ModelForm):

    class Meta:
        model = ImagePost
        fields = ("user","publish_date","image_url","model","model_hash",
                  "hypernetwork","hypernetwork_hash","positive_prompt","negative_prompt",
                  "notes","generation_details","isOnlineService","onlineService")

class ImagePostChangeForm(forms.ModelForm):

    class Meta:
        model = ImagePost
        fields = ("image_url","model","model_hash",
                  "hypernetwork","hypernetwork_hash","positive_prompt","negative_prompt",
                  "notes","generation_details","onlineService")