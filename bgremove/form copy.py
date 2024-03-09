from django.forms import ModelForm
from django import forms
from django.forms import TextInput, FileInput
from .models import PhotoUpload
from PIL import Image
from rembg import remove
import requests
from requests.adapters import Retry, HTTPAdapter


from django import forms
from django.core.files import File



class UploadForm(ModelForm):
    """Feedback form"""

    class Meta:
        model = PhotoUpload
        fields = ["image"]
        widgets = {
            "image": FileInput(
                attrs={
                    "class": "form-control form-control-lg ",
                    "style": " ",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(UploadForm, self).__init__(*args, **kwargs)
        self.fields["image"].label = ""

    def save(self, commit=False):
        photo = super(UploadForm, self).save()
        image_file = Image.open(photo.image)
        output = remove(image_file)  # remove background using rembg
        output_path = photo.image.path
        output.save(output_path, "PNG")

     
        return photo
