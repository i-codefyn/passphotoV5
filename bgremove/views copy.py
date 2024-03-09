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

def download_file(request, pk):
    uploaded_file = PhotoUpload.objects.get(id__gte=pk)
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
