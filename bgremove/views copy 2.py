from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# redirects Imports
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.models import User

from bgremove import app_setting

from .models import PhotoUpload
from .form import UploadForm

# Generic Views Imports
from django.views.generic import (
    ListView,
    DetailView,
    DeleteView,
    UpdateView,
    CreateView,
    RedirectView,
    TemplateView,
)
import os
from django.http import HttpResponse
from django.conf import settings
from django.utils._os import safe_join
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from PIL import Image,ImageOps
 
def image_view(request, pk):
    obj = PhotoUpload.objects.get(pk=pk)
    filename = Image.open(File(obj.file))
   
    try:
        image_file = storage.open(filename, 'rb')
        file_content = image_file.read()
    except:
        filename = 'no_image.gif'
        path = safe_join(os.path.abspath(settings.MEDIA_ROOT), filename)
        if not os.path.exists(path):
            raise ObjectDoesNotExist
        no_image = open(path, 'rb')
        file_content = no_image.read()

    response = HttpResponse(file_content, mimetype="image/jpeg")
    response['Content-Disposition'] = 'inline; filename=%s'%filename
    return response

def download_file(request, pk):
    uploaded_file = PhotoUpload.objects.get(pk=pk)
    response = HttpResponse(uploaded_file.image, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename="{uploaded_file.image.name}"'
    return response

class FileDeleteView(SuccessMessageMixin, DeleteView):
    template_name = "bgremove/bgremove_output." + app_setting.TEMPLATE_EXTENSION
    model = PhotoUpload
    context_object_name = "delete"
    success_url = reverse_lazy("bgremove:output_list")
    success_message = "Item Deleted Successfully !"


class OutputListView(LoginRequiredMixin,ListView):
    template_name = "bgremove/bgremove_output." + app_setting.TEMPLATE_EXTENSION
    model = PhotoUpload
    context_object_name = "photos"


class UploadView(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    model = PhotoUpload
    form_class = UploadForm
    template_name = "bgremove/bgremove_index." + app_setting.TEMPLATE_EXTENSION
    success_url = reverse_lazy("bgremove:output_list")
    success_message = 'Proccess Complete ! Download Now'

class OutputView(LoginRequiredMixin,DetailView):
    model = PhotoUpload
    template_name = "bgremove/bgremove_output_detail." + app_setting.TEMPLATE_EXTENSION
    context_object_name = "photos"
