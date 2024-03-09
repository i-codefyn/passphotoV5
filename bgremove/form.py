from django.forms import ModelForm
from django import forms
from django.forms import TextInput, FileInput
from .models import BgRemove
from PIL import Image
from rembg import remove
import requests
from requests.adapters import Retry, HTTPAdapter

from datetime import datetime
from django import forms
from django.core.files import File

# from django.core.files.storage import default_storage as storage
# from cloudinary_storage.storage import MediaCloudinaryStorage as storage

def get_upload_path(instance, filename):
    """Return timestamp filename for user uploaded files."""

    ext = filename.split(".")[-2]
    time_stamp = datetime.today().strftime("%Y%m%d_%H%M%S")
    folder = datetime.today().strftime("%Y/%m")
    image_path = f"{folder}/{time_stamp}.{ext}"
    return image_path

class BgRemoveForm(ModelForm):
    """Feedback form"""

    class Meta:
        model = BgRemove
        fields = ["image"]
        widgets = {
            "image": FileInput(
                attrs={
                    "class": "form-controll",
                    "id": "image",
                    "type": "file",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(BgRemoveForm, self).__init__(*args, **kwargs)
        self.fields["image"].label = ""

    def save(self, commit=False):
    
        photo = super(BgRemoveForm, self).save()
        image = Image.open(photo.image)
        # output = remove(image)  # remove background using rembg
        image.save("passphoto.png","png")
        return photo
