from datetime import datetime
import uuid

from django.db import models
from django.urls import reverse


def get_upload_path(instance, filename):
    """Return timestamp filename for user uploaded files."""

    ext = filename.split(".")[-2]
    time_stamp = datetime.today().strftime("%Y%m%d_%H%M%S")
    folder = datetime.today().strftime("%Y/%m")
    image_path = f"{folder}/{time_stamp}.{ext}"
    return image_path


class PhotoUpload(models.Model):
    """
    A class representing user activity

    Uploading image to remove its background and downloading.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=get_upload_path)
    output = models.ImageField(upload_to=get_upload_path)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Photo Upload"
        verbose_name_plural = "Photo Uploads"

    def __str__(self) -> str:
        return str(self.image)

    def get_absolute_url(self):
        return reverse("bgremove:output", args=[str(self.id)])
