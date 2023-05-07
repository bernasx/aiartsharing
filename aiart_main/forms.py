from django import forms
from .models import ImagePostReport
class ImagePostReportForm(forms.ModelForm):

    class Meta:
        model = ImagePostReport
        fields = ("report_option","other_option",)
        labels = {
            "report_option":'Please select an option',
            "other_option":"Explain why you're reporting this post",
        }
