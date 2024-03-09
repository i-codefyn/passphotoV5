from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
# rembg
# from rembg import remove
# redirects Imports
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.models import User
import math
import uuid
from .models import PhotoMaker
from photomaker import app_setting
from .forms import PhotoForm,PassPhotoMakerForm
from base64 import b64encode
from .utils import (
    ShowPDF,
)

from django.core.files import File
from PIL import Image,ImageOps,ImageEnhance

# Generic Views Imports
from django.views.generic import (
    View,
    ListView,
    DetailView,
    DeleteView,
    CreateView,
    TemplateView,
)
from django.http import JsonResponse

import os
import io
import base64
import tempfile
from pathlib import Path
from django.http import FileResponse
from Config import settings
from django.http import HttpResponse



class Terms(TemplateView):
    template_name = "terms." + app_setting.TEMPLATE_EXTENSION


class Privacy(TemplateView):
    template_name = "privacy." + app_setting.TEMPLATE_EXTENSION

    
class PassPhoto(LoginRequiredMixin,DetailView):
    template_name = "photo_out/6pcsd.html"
    model = PhotoMaker
    context_object_name = "photos"
    

class PhotosOutputList(LoginRequiredMixin,View):
    """DETAIL VIEWS"""

    template_name = "photomaker/output." + app_setting.TEMPLATE_EXTENSION
    login_url = reverse_lazy("account_login")
    model = PhotoMaker
    
    
    def get(self, request):
        template_name = "output." + app_setting.TEMPLATE_EXTENSION
        login_url = reverse_lazy("account_login")
        contex = {
            "page_title": 'Photos List',
          
            'photos':self.model.objects.filter(
            created_by=self.request.user
        )
        }

        return render(self.request, self.template_name, contex)
   
    def post(self, request, *args, **kwargs):
        if request.method == "POST" or None:
            object_ids = request.POST.getlist('id[]')
            for i in range(len(object_ids)):
                images = []
                for pk in object_ids:
                    obj = self.model.objects.get(pk=pk)
                    img = Image.open(File(obj.file))
                        #bg remove.
                    # im = remove(image)
                    # im = im.convert("RGBA")   # it had mode P after DL it from OP
                    # if im.mode in ('RGBA', 'LA'):
                    #     background = Image.new(im.mode[:-1], im.size, color="white")
                    #     background.paste(im, im.split()[-1]) # omit transparency
                    #     im = background

                    # im.convert("RGB")
                    # border color
                    color = "black"
                    # top, right, bottom, left
                    border = (5, 5, 5, 5)
                    img_enhancer = ImageEnhance.Brightness(img)
                    factor = 1.1
                    enhanced_output = img_enhancer.enhance(factor)
                    new_resized_im = enhanced_output.resize((int(1.3 * 300), int(1.6 * 300)), Image.Resampling.LANCZOS)
                    bordered_img = ImageOps.expand(new_resized_im, border=border, fill=color)
                    resized_image = add_margin(bordered_img, 5, 7, 5, 7, (255, 255, 255))
                    images.append(resized_image)
                    images.append(resized_image)
                    images.append(resized_image)
                    images.append(resized_image)
                    images.append(resized_image)
                    images.append(resized_image)
               
                pass_photo  = get_multi_pass_photo(images,n_rows=(len(object_ids)))
                buffer = io.BytesIO()
                pass_photo.save(buffer, format = "JPEG")
                img_str = base64.b64encode(buffer.getvalue())
                return HttpResponse(img_str)
               
               
class FileDeleteView(LoginRequiredMixin,SuccessMessageMixin, DeleteView):
    template_name = "index." + app_setting.TEMPLATE_EXTENSION
    model = PhotoMaker
    context_object_name = "delete"
    success_url = reverse_lazy("photo:pass_photo_list")
    success_message = "Item Deleted Successfully !"


class HomeView(TemplateView):
    template_name = "index." + app_setting.TEMPLATE_EXTENSION


class PhotosCreateView(LoginRequiredMixin,SuccessMessageMixin, CreateView):
    """Views"""

    model = PhotoMaker
    form_class =  PassPhotoMakerForm
    template_name = "photomaker/index_photo_maker." + app_setting.TEMPLATE_EXTENSION
    page_title = "Photos List"
    success_url = reverse_lazy("photo:pass_photo_list")
    success_message = "Passport Photo is Ready for Download"

    def get(self, request, *args, **kwargs):

        form = self.form_class()
        contex = {
            "form": form,
            "page_title": self.page_title,
        }

        return render(self.request, self.template_name, contex)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None, request.FILES or None)
        user = self.request.user
        if request.method == "POST":
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("photo:pass_photo_list")

    def form_valid(self, form):
        """
        If the form is valid return HTTP 200 status
        code along with name of the user
        """

        form.instance.created_by = self.request.user
        form.save()
        # messages.success(self.request, "Passport Photo is ready to download ")
        # return HttpResponseRedirect(self.get_success_url())
        return JsonResponse({'message': 'success'})
   

    def form_invalid(self, form):
        return render(
            self.request,
            self.template_name,
            {
                "form": form,
            },
        )
    

@login_required
def pass_photo_single(request, pk):
    """Photo For SSC """
    # Get the image data from the database.
    photo = get_object_or_404(PhotoMaker, pk=pk)
    file_name = "passphoto_single.jpg"
    img = Image.open(File(photo.file)).convert("RGB")
    #bg remove.
    # im = remove(new_img)
    # im = im.convert("RGBA")   # it had mode P after DL it from OP
    # if im.mode in ('RGBA', 'LA'):
    #     background = Image.new(im.mode[:-1], im.size, color="white")
    #     background.paste(im, im.split()[-1]) # omit transparency
    #     im = background
    # im.convert("RGB")
    # border color
    color = "black"
    # top, right, bottom, left
    border = (5, 5, 5, 5)
    #brightness.
    img_enhancer = ImageEnhance.Brightness(img)
    factor = 1.1
    enhanced_output = img_enhancer.enhance(factor)
    new_resized_im = enhanced_output.resize((int(1.3 * 300), int(1.6 * 300)), Image.Resampling.LANCZOS)
    bordered_img = ImageOps.expand(new_resized_im, border=border, fill=color)
    response = HttpResponse(content_type="'image/jpeg'")
    bordered_img.save(response, 'jpeg')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(file_name)

    return response



@login_required
def pass_photo_full_4by6(request, pk):
    """Photo 42 """
    photo = get_object_or_404(PhotoMaker, pk=pk)
    file_name = "passphoto_9pcs.jpg"
    # Get the image data from the database.
    img = Image.open(File(photo.file))
    # Save the image to a file.
    # im = remove(new_img)

    # im = im.convert("RGBA")   # it had mode P after DL it from OP
    # if im.mode in ('RGBA', 'LA'):
    #     background = Image.new(im.mode[:-1], im.size, color="white")
    #     background.paste(im, im.split()[-1]) # omit transparency
    #     im = background

    # im.convert("RGB")
    # border color
    color = "black"
    # top, right, bottom, left
    border = (5, 5, 5, 5)
    
    img_enhancer = ImageEnhance.Brightness(img)
    factor = 1.1
    enhanced_output = img_enhancer.enhance(factor)
    new_resized_im = enhanced_output.resize((int(1.26 * 300), int(1.58 * 300)), Image.Resampling.LANCZOS)
    bordered_img = ImageOps.expand(new_resized_im, border=border, fill=color)
    resized_image = add_margin(bordered_img, 5, 5, 5, 5, (255, 255, 255))
    pass_photo  = get_multi_pass_photo_4by6(im_list=[resized_image, resized_image, resized_image, resized_image,resized_image,
                                    
                                                resized_image, resized_image,resized_image,resized_image], n_rows=3)
  
    response = HttpResponse(content_type="'image/jpeg'")
    pass_photo.save(response, 'jpeg')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(file_name)

    return response


def get_multi_pass_photo_4by6(im_list, n_rows):
    n_cols = math.ceil(len(im_list) / n_rows)
    width, height = int(4 * 300), int(6 * 300) # A4 at 300dpi
    fourby6_sheet = Image.new('RGB', (width, height),(255, 255, 255))
    pos_x = 0
    pos_y = 0
    for i in range(len(im_list)):
        im = im_list[i]
        fourby6_sheet.paste(im, (pos_y, pos_x))
        pos_y += im.width
        if (i + 1) % n_cols == 0:
            # new row
            pos_x += im.height
            pos_y = 0

    return fourby6_sheet

@login_required
def pass_photo_full(request, pk):
    """Photo 42 """
    photo = get_object_or_404(PhotoMaker, pk=pk)
    file_name = "passphoto_42pcs.jpg"
    # Get the image data from the database.
    img = Image.open(File(photo.file))
    # Save the image to a file.
    # im = remove(new_img)

    # im = im.convert("RGBA")   # it had mode P after DL it from OP
    # if im.mode in ('RGBA', 'LA'):
    #     background = Image.new(im.mode[:-1], im.size, color="white")
    #     background.paste(im, im.split()[-1]) # omit transparency
    #     im = background

    # im.convert("RGB")
    # border color
    color = "black"
    # top, right, bottom, left
    border = (5, 5, 5, 5)
    img_enhancer = ImageEnhance.Brightness(img)
    factor = 1.1
    enhanced_output = img_enhancer.enhance(factor)
    new_resized_im = enhanced_output.resize((int(1.3 * 300), int(1.6 * 300)), Image.Resampling.LANCZOS)
    bordered_img = ImageOps.expand(new_resized_im, border=border, fill=color)
    resized_image = add_margin(bordered_img, 5, 7, 5, 7, (255, 255, 255))
    pass_photo  = get_multi_pass_photo(im_list=[resized_image, resized_image, resized_image, resized_image,
                                                resized_image, resized_image, resized_image, resized_image,
                                                resized_image, resized_image, resized_image, resized_image,
                                                resized_image, resized_image, resized_image, resized_image,  
                                                resized_image, resized_image, resized_image, resized_image,
                                                resized_image, resized_image, resized_image, resized_image,
                                                resized_image, resized_image,
                                                resized_image, resized_image, resized_image, resized_image,
                                                resized_image, resized_image, 
                                                resized_image, resized_image, resized_image, resized_image,
                                                resized_image, resized_image,  
                                                resized_image, resized_image,resized_image,resized_image], n_rows=7)
  
    response = HttpResponse(content_type="'image/jpeg'")
    pass_photo.save(response, 'jpeg')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(file_name)

    return response


@login_required
def pass_photo_36(request, pk):
    """Photo 36 """
    photo = get_object_or_404(PhotoMaker, pk=pk)
    file_name = "passphoto_36pcs.jpg"
    img = Image.open(File(photo.file))
    # # remove bg.
    # im = remove(new_img) 
    # im = im.convert("RGBA")   # it had mode P after DL it from OP
    # if im.mode in ('RGBA', 'LA'):
    #     background = Image.new(im.mode[:-1], im.size, color="white")
    #     background.paste(im, im.split()[-1]) # omit transparency
    #     im = background

    # im.convert("RGB")
    # border color
    color = "black"
    # top, right, bottom, left
    border = (5, 5, 5, 5)
    img_enhancer = ImageEnhance.Brightness(img)
    factor = 1.1
    enhanced_output = img_enhancer.enhance(factor)
    new_resized_im = enhanced_output.resize((int(1.3 * 300), int(1.6 * 300)), Image.Resampling.LANCZOS)
    bordered_img = ImageOps.expand(new_resized_im, border=border, fill=color)
    resized_image = add_margin(bordered_img, 5, 7, 5, 7, (255, 255, 255))
    pass_photo  = get_multi_pass_photo(im_list=[resized_image, resized_image, resized_image, resized_image,
                                                resized_image, resized_image, resized_image, resized_image,
                                                resized_image, resized_image, resized_image, resized_image,
                                                resized_image, resized_image, resized_image, resized_image,  
                                                resized_image, resized_image, resized_image, resized_image,
                                                resized_image, resized_image, resized_image, resized_image,
                                                resized_image, resized_image,
                                                resized_image, resized_image, resized_image, resized_image,
                                                resized_image, resized_image,   
                                                resized_image, resized_image,resized_image,resized_image], n_rows=6)
  
    response = HttpResponse(content_type="'image/jpeg'")
    pass_photo.save(response, 'jpeg')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(file_name)

    return response


@login_required
def pass_photo_30(request, pk):
    """Photo 30 """
    photo = get_object_or_404(PhotoMaker, pk=pk)
    file_name = "passphoto_30pcs.jpg"
    # Get the image data from the database.
    img = Image.open(File(photo.file))
    # Save the image to a file.
    # im = remove(new_img)

    # im = im.convert("RGBA")   # it had mode P after DL it from OP
    # if im.mode in ('RGBA', 'LA'):
    #     background = Image.new(im.mode[:-1], im.size, color="white")
    #     background.paste(im, im.split()[-1]) # omit transparency
    #     im = background

    # im.convert("RGB")
    # border color
    color = "black"
    # top, right, bottom, left
    border = (5, 5, 5, 5)
    img_enhancer = ImageEnhance.Brightness(img)
    factor = 1.1
    enhanced_output = img_enhancer.enhance(factor)
    new_resized_im = enhanced_output.resize((int(1.3 * 300), int(1.6 * 300)), Image.Resampling.LANCZOS)
    bordered_img = ImageOps.expand(new_resized_im, border=border, fill=color)
    resized_image = add_margin(bordered_img, 5, 7, 5, 7, (255, 255, 255))
    pass_photo  = get_multi_pass_photo(im_list=[resized_image, resized_image, resized_image, resized_image,
                                                resized_image, resized_image, resized_image, resized_image,
                                                resized_image, resized_image, resized_image, resized_image,
                                                resized_image, resized_image, resized_image, resized_image,  
                                                resized_image, resized_image, resized_image, resized_image,
                                                resized_image, resized_image, resized_image, resized_image,
                                                resized_image, resized_image,  
                                                resized_image, resized_image,resized_image,resized_image], n_rows=5)
  
    response = HttpResponse(content_type="'image/jpeg'")
    pass_photo.save(response, 'jpeg')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(file_name)

    return response

@login_required
def pass_photo_24(request, pk):
    """Photo 24 """
    photo = get_object_or_404(PhotoMaker, pk=pk)
    file_name = "passphoto_18pcs.jpg"
    img = Image.open(File(photo.file))
    # Save the image to a file.
    # im = remove(new_img)

    # im = im.convert("RGBA")   # it had mode P after DL it from OP
    # if im.mode in ('RGBA', 'LA'):
    #     background = Image.new(im.mode[:-1], im.size, color="white")
    #     background.paste(im, im.split()[-1]) # omit transparency
    #     im = background

    # im.convert("RGB")
    # border color
    color = "black"
    # top, right, bottom, left
    border = (5, 5, 5, 5)
    img_enhancer = ImageEnhance.Brightness(img)
    factor = 1.1
    enhanced_output = img_enhancer.enhance(factor)
    new_resized_im = enhanced_output.resize((int(1.3 * 300), int(1.6 * 300)), Image.Resampling.LANCZOS)
    bordered_img = ImageOps.expand(new_resized_im, border=border, fill=color)
    resized_image = add_margin(bordered_img, 5, 7, 5, 7, (255, 255, 255))
    pass_photo  = get_multi_pass_photo(im_list=[resized_image, resized_image, resized_image, resized_image,
                                                resized_image, resized_image, resized_image, resized_image,
                                                resized_image, resized_image, resized_image, resized_image,
                                                resized_image, resized_image, resized_image, resized_image,  
                                                resized_image, resized_image, resized_image, resized_image,
                                                
                                                resized_image, resized_image,resized_image,resized_image], n_rows=4)
  
    response = HttpResponse(content_type="'image/jpeg'")
    pass_photo.save(response, 'jpeg')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(file_name)

    return response

@login_required
def pass_photo_18(request, pk):
    """Photo 18 """
    photo = get_object_or_404(PhotoMaker, pk=pk)
    file_name = "passphoto_18pcs.jpg"
    # Get the image data from the database.
    img = Image.open(File(photo.file))
    # Save the image to a file.

    # border color
    color = "black"
    # top, right, bottom, left
    border = (5, 5, 5, 5)
    img_enhancer = ImageEnhance.Brightness(img)
    factor = 1.1
    enhanced_output = img_enhancer.enhance(factor)
    new_resized_im = enhanced_output.resize((int(1.3 * 300), int(1.6 * 300)), Image.Resampling.LANCZOS)
    bordered_img = ImageOps.expand(new_resized_im, border=border, fill=color)
    resized_image = add_margin(bordered_img, 5, 7, 5, 7, (255, 255, 255))
    pass_photo  = get_multi_pass_photo(im_list=[resized_image, resized_image, resized_image, resized_image,
                                                resized_image, resized_image, resized_image, resized_image,
                                                resized_image, resized_image, 
                                      resized_image, resized_image, resized_image, resized_image, resized_image, 
                                      resized_image,resized_image,resized_image], n_rows=3)
  
    response = HttpResponse(content_type="'image/jpeg'")
    pass_photo.save(response, 'jpeg')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(file_name)

    return response

@login_required
def pass_photo_12(request, pk):
    """Photo 12 """
    photo = get_object_or_404(PhotoMaker, pk=pk)
    file_name = "passphoto_12pcs.jpg"
    # Get the image data from the database.
    img = Image.open(File(photo.file))
    # Save the image to a file.
    # im = remove(new_img)

    # im = im.convert("RGBA")   # it had mode P after DL it from OP
    # if im.mode in ('RGBA', 'LA'):
    #     background = Image.new(im.mode[:-1], im.size, color="white")
    #     background.paste(im, im.split()[-1]) # omit transparency
    #     im = background

    # im.convert("RGB")
    # border color
    color = "black"
    # top, right, bottom, left
    border = (5, 5, 5, 5)
    img_enhancer = ImageEnhance.Brightness(img)
    factor = 1.1
    enhanced_output = img_enhancer.enhance(factor)
    new_resized_im = enhanced_output.resize((int(1.3 * 300), int(1.6 * 300)), Image.Resampling.LANCZOS)
    bordered_img = ImageOps.expand(new_resized_im, border=border, fill=color)
    resized_image = add_margin(bordered_img, 5, 7, 5, 7, (255, 255, 255))
    pass_photo  = get_multi_pass_photo(im_list=[resized_image, resized_image, resized_image, resized_image,
                                      resized_image, resized_image, resized_image, resized_image, resized_image, 
                                      resized_image,resized_image,resized_image], n_rows=2)
  
    response = HttpResponse(content_type="'image/jpeg'")
    pass_photo.save(response, 'jpeg')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(file_name)

    return response


@login_required
def pass_photo_6(request, pk):
    """Photo 6 """
    photo = get_object_or_404(PhotoMaker, pk=pk)
    file_name = "passphoto_6pcs.jpg"
    # Get the image data from the database.
    img = Image.open(File(photo.file))
    # Save the image to a file.
    # im = remove(new_img)

    # im = im.convert("RGBA")   # it had mode P after DL it from OP
    # if im.mode in ('RGBA', 'LA'):
    #     background = Image.new(im.mode[:-1], im.size, color="white")
    #     background.paste(im, im.split()[-1]) # omit transparency
    #     im = background

    # im.convert("RGB")
    # border color
    color = "black"
    # top, right, bottom, left
    border = (5, 5, 5, 5)
    img_enhancer = ImageEnhance.Brightness(img)
    factor = 1.1
    enhanced_output = img_enhancer.enhance(factor)
    new_resized_im = enhanced_output.resize((int(1.3 * 300), int(1.6 * 300)), Image.Resampling.LANCZOS)
    bordered_img = ImageOps.expand(new_resized_im, border=border, fill=color)
    resized_image = add_margin(bordered_img, 5, 7, 5, 7, (255, 255, 255))
    pass_photo  = get_multi_pass_photo(im_list=[resized_image, resized_image, resized_image, resized_image,
                                      resized_image, resized_image], n_rows=1)
    #for download
    response = HttpResponse(content_type="'image/jpeg'")
    pass_photo.save(response, 'jpeg')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(file_name)
 
    return response

def add_margin(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result
   

def get_multi_pass_photo(im_list, n_rows):
    n_cols = math.ceil(len(im_list) / n_rows)
    width, height = int(8.27 * 300), int(11.7 * 300) # A4 at 300dpi
    a4_sheet = Image.new('RGB', (width, height),(255, 255, 255))
    pos_x = 0
    pos_y = 0
    for i in range(len(im_list)):
        im = im_list[i]
        a4_sheet.paste(im, (pos_y, pos_x))
        pos_y += im.width
        if (i + 1) % n_cols == 0:
            # new row
            pos_x += im.height
            pos_y = 0

    return a4_sheet


 
def pass_photo_60(request, pk):
    """Works Export Pdf by id"""
    template_name = "photo_out/6pcs.html"
    photo = PhotoMaker.objects.filter(pk=pk)
    pdf_name = "pass_photo_6pcs.pdf"
    context = {
        "photos": photo,
    }
    return ShowPDF(template_name, context, pdf_name)
