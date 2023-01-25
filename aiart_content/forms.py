from django import forms

from .models import Post


class PostCreationForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ("title","user","publish_date")

class PostChangeForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ("title","publish_date")