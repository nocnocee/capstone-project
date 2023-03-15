from django import forms
from .models import GeneratedImage

class GeneratedImageForm(forms.ModelForm):
    image_path = forms.FileField(required=False)

    class Meta:
        model = GeneratedImage
        fields = ('image_path',)
