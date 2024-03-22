from datetime import datetime
import uuid
from django.conf import settings
import requests

# from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from requests.adapters import Retry, HTTPAdapter

from io import BytesIO
import sys
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
# rembg
from rembg import remove

session = requests.Session()  # to retry failed requests (3 times)
retries = Retry(total=3, backoff_factor=1)
session.mount("http://", HTTPAdapter(max_retries=retries))
session.mount("https://", HTTPAdapter(max_retries=retries))
User = get_user_model()



def get_upload_path(instance, filename):
    """Return timestamp filename for user uploaded files."""

    ext = filename.split(".")[-1]
    time_stamp = datetime.today().strftime("%Y%m%d_%H%M%S")
    folder = datetime.today().strftime("%Y/%m")
    image_path = f"{folder}/{time_stamp}.{ext}"
    return image_path


class PhotoMaker(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.ImageField(upload_to=get_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, default=None, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "photo maker"
        verbose_name_plural = "photos maker"
    
    def __str__(self) -> str:
        return str(self.file)

    def get_absolute_url(self):
        return reverse("photo:photos", args=[str(self.id)])
    
    def save(self):
        # Opening the uploaded image
        img = Image.open(self.file)
        output = BytesIO()
        # Resize/modify the image
        img = img.resize((int(1.3 * 300), int(1.6 * 300)), Image.Resampling.LANCZOS)
        # img = img.resize((400, 600))
        im = remove(img)  # remove background using rembg
        # output_path = photo.file.name

        im = im.convert("RGBA")   # it had mode P after DL it from OP
        if im.mode in ('RGBA', 'LA'):
            background = Image.new(im.mode[:-1], im.size, color="white")
            background.paste(im, im.split()[-1]) # omit transparency
            im = background

        im.convert("RGB")
        # after modifications, save it to the output
        im.save(output, format='jpeg', quality=90)
        output.seek(0)

        # change the imagefield value to be the newley modifed image value
        self.file = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.file.name.split('.')[0], 'image/jpeg',
                                        sys.getsizeof(output), None)

        super(PhotoMaker, self).save()
