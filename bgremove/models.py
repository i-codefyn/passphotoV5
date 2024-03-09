from datetime import datetime
import uuid
import requests

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

from django.conf import settings
session = requests.Session()  # to retry failed requests (3 times)
retries = Retry(total=3, backoff_factor=1)
session.mount("http://", HTTPAdapter(max_retries=retries))
session.mount("https://", HTTPAdapter(max_retries=retries))
User = get_user_model()

# fs = FTPStorage(base_url=settings.FTP_STORAGE_LOCATION)
def get_upload_path(instance, filename):
    """Return timestamp filename for user uploaded files."""

    ext = filename.split(".")[-2]
    time_stamp = datetime.today().strftime("%Y%m%d_%H%M%S")
    folder = datetime.today().strftime("%Y/%m")
    image_path = f"{folder}/{time_stamp}.{ext}"
    return image_path




class BgRemove(models.Model):
    """
    A class representing user activity

    Uploading image to remove its background and downloading.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='media/')
    output = models.ImageField(upload_to='media/')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, default=None, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "BG Remove"
        verbose_name_plural = "Photo Uploads"

    def __str__(self) -> str:
        return str(self.image)
    


    def get_absolute_url(self):
        return reverse("bgremove:output", args=[str(self.id)])
    

    # def save(self):
    #     # Opening the uploaded image
    #     img = Image.open(self.image)
    #     output = BytesIO()


    #     im = remove(img)  # remove background using rembg
    #     # output_path = photo.file.name

    #     # im = im.convert("RGBA")   # it had mode P after DL it from OP
    #     # if im.mode in ('RGBA', 'LA'):
    #     #     background = Image.new(im.mode[:-1], im.size, color="white")
    #     #     background.paste(im, im.split()[-1]) # omit transparency
    #     #     im = background

    #     # im.convert("RGB")
    #     # after modifications, save it to the output
    #     im.save(output, format='png', quality=90)
    #     output.seek(0)

    #     # change the imagefield value to be the newley modifed image value
    #     self.image = InMemoryUploadedFile(output, 'ImageField', "%s.png" % self.image.name.split('.')[0], 'image/png',
    #                                     sys.getsizeof(output), None)

    #     super(BgRemove, self).save()