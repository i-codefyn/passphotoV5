from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# redirects Imports
import time

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.models import User

from bgremove import app_setting

from .models import BgRemove
from .form import BgRemoveForm

# Generic Views Imports
from django.views.generic import (
    ListView,
    DetailView,
    DeleteView,
    UpdateView,
    CreateView,
    RedirectView,
    TemplateView,
    View,
)
import os
from django.http import HttpResponse
from django.conf import settings
from django.utils._os import safe_join
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from PIL import Image,ImageOps

import io
import base64
from rembg import remove
from django.template.loader import render_to_string

import os
import tempfile
from PIL import Image
from django.http import HttpResponse


class ProgressBarUploadView(View):
    def get(self, request):
        photos_list = BgRemove.objects.all()
        return render(self.request, 'bgremove/bgremove_index.html', {'photos': photos_list})

    def post(self, request):
        time.sleep(1)  # You don't need this line. This is just to delay the process so you can see the progress bar testing locally.
        form = BgRemoveForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            image = request.FILES.get('image')
            # Get the image from the form
            # image = request.FILES['image']

            # Open the image
            img = Image.open(image)

                # Resize the image
            im = remove(img)

                # # Save the image to a temporary file
                # temp_file = tempfile.NamedTemporaryFile(suffix=".png")
                # im.save(temp_file)

                # # Send the image to the user
                # response = HttpResponse()
                # response['Content-Type'] = 'image/jpeg/png'
                # response.write(temp_file.read())
                # temp_file.close()
            buffer = io.BytesIO()
            im.save(buffer, format = "PNG")
            img_str = base64.b64encode(buffer.getvalue())
            
            # file_name = "passphoto.in_bgremoved.png"
            # response = HttpResponse(content_type="'image/png'")
            # im.save(response, 'png')
            # response['Content-Disposition'] = 'attachment; filename={0}'.format(file_name)
            #     # response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            # return response
            # photo = form.save()
            data = {'is_valid': True, 'img': img_str}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)
    
class DragAndDropUploadView(View):
    def get(self, request):
        photos_list =BgRemove.objects.all()
        return render(self.request, 'bgremove/bgremove_index.html', {'photos': photos_list})

    def post(self, request):
        form = BgRemoveForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.image.name, 'url': photo.image.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)

def resize_and_download_image(request):
        if request.method == 'POST':
            image = request.FILES.get('image')
            # Get the image from the form
            # image = request.FILES['image']
            # Open the image
            im = Image.open(image)
            # Resize the image
            im = im.resize((200, 200))
            # Save the image to a temporary file
            temp_file = tempfile.NamedTemporaryFile()
            im.save(temp_file)
            # Send the image to the user
            response = HttpResponse()
            response['Content-Type'] = 'image/jpeg'
            response.write(temp_file.read())
            temp_file.close()

            return response

def upload(request):
    if request.method == 'POST':
        if request.is_ajax():
            image = request.FILES.get('image')
            uploaded_image = BgRemove(image= image)
            uploaded_image.save()
            photo = BgRemove.objects.first()# This will give last inserted photo
        return HttpResponse(photo)

def image_view(request):
    template_name = "bgremove/bgremove_output." + app_setting.TEMPLATE_EXTENSION
             
    obj = BgRemove.objects.all()
    images = []
    for im in obj:
        img = Image.open(File(im.image))
        images.append(img)
    
    buffer = io.BytesIO()
    img.save(buffer, format = "png")
    img_str = base64.b64encode(buffer.getvalue())
    
    context = {
            'photos':img_str
           
    }
    return render(request, template_name, context)
    

def download_file(request, pk):
    uploaded_file = BgRemove.objects.get(pk=pk)
    image = Image.open(uploaded_file.image)

    # output = remove(image)  # remove background using rembg
    # # response = HttpResponse(output, content_type='application/force-download')
    file_name = "passphoto.in_bgremoved.png"
    response = HttpResponse(content_type="'image/png'")
    image.save(response, 'png')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(file_name)
    # response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    return response

class FileDeleteView(SuccessMessageMixin, DeleteView):
    template_name = "bgremove/bgremove_output." + app_setting.TEMPLATE_EXTENSION
    model = BgRemove
    context_object_name = "delete"
    success_url = reverse_lazy("bgremove:output_list")
    success_message = "Item Deleted Successfully !"


class OutputListView(LoginRequiredMixin,View):
    template_name = "bgremove/bgremove_output." + app_setting.TEMPLATE_EXTENSION
    model = BgRemove
    context_object_name = "photos"
    login_url = reverse_lazy("account_login")
    def get(self, request):
        
        contex = {
            "page_title": 'Photos List',
            'photos':self.model.objects.filter(
            created_by=self.request.user
        ),
        }

        return render(self.request, self.template_name, contex)
    
    
class UploadView(SuccessMessageMixin,View):

    """DETAIL VIEWS"""

    model = BgRemove
    form_class = BgRemoveForm
    template_name = "bgremove/bgremove_index." + app_setting.TEMPLATE_EXTENSION
    login_url = reverse_lazy("account_login")
   
    def get(self, request):
        contex = {
            "page_title": 'Photos List',
            "form":self.form_class,
        }
        return render(self.request, self.template_name, contex)
   
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None, request.FILES or None)
        user = self.request.user
        if request.method == "POST":
            if form.is_valid():
                # image = request.FILES.get('image')
                # # Get the image from the form
                image = request.FILES['image']

                # # # Open the image
                img = Image.open(image)

                # # # Resize the image
                im = remove(img)

                # # Save the image to a temporary file
                # temp_file = tempfile.NamedTemporaryFile(suffix=".png")
                # im.save(temp_file)

                # # Send the image to the user
                # response = HttpResponse()
                # response['Content-Type'] = 'image/jpeg/png'
                # response.write(temp_file.read())
                # temp_file.close()
                
                # file_name = "passphoto.in_bgremoved.png"
                # response = HttpResponse(content_type="'image/png'")
                # im.save(response, 'png')
                # response['Content-Disposition'] = 'attachment; filename={0}'.format(file_name)
                # # response['Content-Disposition'] = f'attachment; filename="{file_name}"'
                # messages.success(request, 'File upload successful')
                # return response
                buffer = io.BytesIO()
                im.save(buffer, format = "PNG")
                img_str = base64.b64encode(buffer.getvalue())
                # return HttpResponse(img_str)
                return HttpResponse(img_str)
            else:
                return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("bgremove:output_list")

    def form_valid(self, form):
        """
        If the form is valid return HTTP 200 status
        code along with name of the user
        """

        form.instance.created_by = self.request.user
        form.save(commit=False)
        # photo=BgRemove.objects.first()# This will give last inserted photo
        # return HttpResponse(photo)
        messages.success(self.request, "Passport Photo is ready to download ")
        
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return render(
            self.request,
            self.template_name,
            {
                "form": form,
            },
        )
               
            
    

class OutputView(LoginRequiredMixin,DetailView):
    model = BgRemove
    template_name = "bgremove/bgremove_output_detail." + app_setting.TEMPLATE_EXTENSION
    context_object_name = "photos"
