from django import forms
from .models import ImagePost


class ImagePostCreationForm(forms.ModelForm):

    class Meta:
        model = ImagePost
        fields = ("image_url","model",
                  "hypernetwork","positive_prompt","negative_prompt",
                  "notes","generation_details","isOnlineService","onlineService")
        labels = {
            "image_url":'Image URL',
            "model":"Model",
            "hypernetwork": "Hypernetwork",
            "positive_promopt":"Positive Prompt",
            "negative_prompt":"Negative Prompt",
            "notes":"Notes",
            "generation_details": "Generation Details",
            "isOnlineService": "Generated in an Online Service?",
            "onlineService": "Online Service"
        }

class ImagePostChangeForm(forms.ModelForm):

    class Meta:
        model = ImagePost
        fields = ("image_url","model",
                  "hypernetwork","positive_prompt","negative_prompt",
                  "notes","generation_details","onlineService")
        labels = {
            "image_url":'Image URL',
            "model":"Model",
            "hypernetwork": "Hypernetwork",
            "positive_promopt":"Positive Prompt",
            "negative_prompt":"Negative Prompt",
            "notes":"Notes",
            "generation_details": "Generation Details",
            "isOnlineService": "Generated in an Online Service?",
            "onlineService": "Online Service"
        }


class SimpleSearchForm(forms.Form):
    keyword = forms.CharField(label="Search for anything", max_length=100, required=True)
    search_type = forms.CharField(widget=forms.HiddenInput, initial='simple')

    