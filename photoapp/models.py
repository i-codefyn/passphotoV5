from django.db import models

class Image(models.Model):
    image_data = models.TextField()  # Store the image data URI as text