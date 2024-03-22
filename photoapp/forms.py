
from django import forms



class PhotosCreaterForm(forms.Form):
    image = forms.FileField()
    image.widget.attrs.update({
        "class": "form-control",
        "id": "image",
        "multiple": "True",
        })
    image.label = ''


                              

