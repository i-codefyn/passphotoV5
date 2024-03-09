import PIL
from io import BytesIO
import os
from django.core.files import File
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
from rembg import remove
import requests
from requests.adapters import Retry, HTTPAdapter

from django import forms
from django.core.files import File

from .models import PhotoMaker


class CheckBoxForm(forms.Form): 
    checkbox = forms.BooleanField( initial='{{ photos.id }}' ,required = True, disabled = False, 
                               widget=forms.widgets.CheckboxInput( attrs={
                                   'class': 'checkbox-inline',
                                   'name':"photo_id[]",
                                    
                                    }), 
                              
                               )


class PhotoForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = PhotoMaker
        fields = (
            "file",
            "x",
            "y",
            "width",
            "height",
        )
        widgets = {
            "file": forms.FileInput(
                attrs={
                    "accept": "image/*" ,
                    "class":"form-control form-control-lg"
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super(PhotoForm, self).__init__(*args, **kwargs)
        self.fields["file"].label = ""

    def save(self, commit=False):
        photo = super(PhotoForm, self).save()

        x = self.cleaned_data.get("x")
        y = self.cleaned_data.get("y")
        w = self.cleaned_data.get("width")
        h = self.cleaned_data.get("height")

        image = PIL.Image.open(photo.file)
        cropped_image = image.crop((x, y, w + x, h + y))
        img = cropped_image.resize((int(1.3 * 300), int(1.6 * 300)), PIL.Image.Resampling.LANCZOS)
        im = remove(img)  # remove background using rembg
        output_path = photo.file.name
       

        im = im.convert("RGBA")   # it had mode P after DL it from OP
        if im.mode in ('RGBA', 'LA'):
            background = Image.new(im.mode[:-1], im.size, color="white")
            background.paste(im, im.split()[-1]) # omit transparency
            im = background

        im.convert("RGB")
        im.save()
        return photo


