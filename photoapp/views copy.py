
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


# redirects Imports
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.models import User


from photoapp import app_setting
from photoapp.forms import PhotosCreaterForm

# Generic Views Imports
from django.views.generic import (
    View,

)
import base64
from django.views.decorators.csrf import csrf_exempt

import math
import io
import os
import cv2
import numpy as np
import PIL
# rembg
from rembg import remove

class BgRemoveView(SuccessMessageMixin,View):

    """DETAIL VIEWS"""

    template_name = "photoapp/bg_remove." + app_setting.TEMPLATE_EXTENSION
    login_url = reverse_lazy("account_login")
   
    def get(self, request):
        contex = {
            "page_title": 'Bg Remove',
        }
        return render(self.request, self.template_name, contex)
   
    def post(self, request, *args, **kwargs):

        if request.method == "POST":
            
            if 'image' in request.FILES:
                image = request.FILES['image']
                img = PIL.Image.open(image)
                processed_image = remove(img)
                buffered = io.BytesIO()
                processed_image.save(buffered, format="PNG")
                processed_image_bytes = buffered.getvalue()
                # Encode the processed image bytes to base64 and decode to string
                processed_image_base64 = base64.b64encode(processed_image_bytes).decode('utf-8')
                return JsonResponse({'image': processed_image_base64})
            else:
                return JsonResponse({'error': 'No image provided'},status=400)


        else:
            return JsonResponse({'error': 'No image provided'}, status=405)



class PassPhotosCreaterView(SuccessMessageMixin,View):

    """DETAIL VIEWS"""

    template_name = "photoapp/index_photoapp." + app_setting.TEMPLATE_EXTENSION
    login_url = reverse_lazy("account_login")
   
    def get(self, request):
        contex = {
            "page_title": 'Photos List',
        }
        return render(self.request, self.template_name, contex)
   
    def post(self, request, *args, **kwargs):

        if request.method == "POST" or None:

            image_file = request.FILES.getlist('files[]')
            # Handle background color
            bg_color = request.POST.get('bg_color', None)
        
            if bg_color == "white":
                # Process the background color
                img_list = []
                for imgs in image_file :
                
                    # Read the image
                    img_array = imgs.read()
                    nparr = np.fromstring(img_array, np.uint8)
                    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                    # Convert image to grayscale
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  
                    # Load the pre-trained face detector
                    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

                    # Detect faces in the image
                    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

                    # Crop the first detected face
                    if len(faces) > 0:
                        (x, y, w, h) = faces[0]
                        # Crop and store each face with increased area
                        # for i, (x, y, w, h) in enumerate(faces):
                        # Expand the bounding box
                        x -= int(0.4 * w + 50)
                        y -= int(0.4 * h + 50)
                        w += int(0.8 * w + 100)
                        h += int(1.2 * h + 100)

                        # Ensure the bounding box stays within the image bounds
                        x = max(x, 0)
                        y = max(y, 0)
                        w = min(w, img.shape[1] - x)
                        h = min(h, img.shape[0] - y)
                        # Crop the face
                        cropped_face = img[y:y+h, x:x+w]
                        # converted from BGR to RGB 
                        color_coverted = cv2.cvtColor(cropped_face, cv2.COLOR_BGR2RGB) 
  
                        # Displaying the Scanned Image by using cv2.imshow() method 
                        # Displaying the converted image 
                        pil_image = PIL.Image.fromarray(color_coverted)
                        #bg remove.
                    
                        im = remove(pil_image)
                        im = im.convert("RGBA")   # it had mode P after DL it from OP
                        if im.mode in ('RGBA', 'LA'):
                            background = PIL.Image.new(im.mode[:-1], im.size, color="white")
                            background.paste(im, im.split()[-1]) # omit transparency
                            im = background

                        im.convert("RGB")
                        color = "black"
                        # top, right, bottom, left
                        border = (5, 5, 5, 5)
                        img_enhancer = PIL.ImageEnhance.Brightness(im)
                        factor = 1.1
                        enhanced_output = img_enhancer.enhance(factor)
                        new_resized_im = enhanced_output.resize((int(1.3 * 300), int(1.6 * 300)), PIL.Image.Resampling.LANCZOS)
                        bordered_img = PIL.ImageOps.expand(new_resized_im, border=border, fill=color)
                        resized_image = add_margin(bordered_img, 5, 7, 5, 7, (255, 255, 255))

                    img_list.append(resized_image)
                    img_list.append(resized_image)
                    img_list.append(resized_image)
                    img_list.append(resized_image)
                    img_list.append(resized_image)
                    img_list.append(resized_image)


                pass_photo  = get_multi_pass_photo(img_list,n_rows=(len(image_file)))
                open_cv_image = np.array(pass_photo)
                # Convert RGB to BGR
                open_cv_image = open_cv_image[:, :, ::-1].copy() 
                retval, buffer = cv2.imencode('.jpg', open_cv_image)
                base64_image = base64.b64encode(buffer).decode('utf-8')
                return JsonResponse({'output': base64_image})
            else:
                # Handle case where background color is not provided
                img_list = []
                for imgs in image_file :
                
                    # Read the image
                    img_array = imgs.read()
                    nparr = np.fromstring(img_array, np.uint8)
                    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                    # Convert image to grayscale
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  
                    # Load the pre-trained face detector
                    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

                    # Detect faces in the image
                    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

                    # Crop the first detected face
                    if len(faces) > 0:
                        (x, y, w, h) = faces[0]
                        # Crop and store each face with increased area
                        # for i, (x, y, w, h) in enumerate(faces):
                        # Expand the bounding box
                        x -= int(0.4 * w + 50)
                        y -= int(0.4 * h + 50)
                        w += int(0.8 * w + 100)
                        h += int(1.2 * h + 100)

                        # Ensure the bounding box stays within the image bounds
                        x = max(x, 0)
                        y = max(y, 0)
                        w = min(w, img.shape[1] - x)
                        h = min(h, img.shape[0] - y)
                        # Crop the face
                        cropped_face = img[y:y+h, x:x+w]
                        # converted from BGR to RGB 
                        color_coverted = cv2.cvtColor(cropped_face, cv2.COLOR_BGR2RGB) 
  
                        # Displaying the Scanned Image by using cv2.imshow() method 
                        # Displaying the converted image 
                        pil_image = PIL.Image.fromarray(color_coverted)
                        #bg remove.
                    
                        # im = remove(pil_image)
                        # im = im.convert("RGBA")   # it had mode P after DL it from OP
                        # if im.mode in ('RGBA', 'LA'):
                        #     background = PIL.Image.new(im.mode[:-1], im.size, color="white")
                        #     background.paste(im, im.split()[-1]) # omit transparency
                        #     im = background

                        # im.convert("RGB")
                        color = "black"
                        # top, right, bottom, left
                        border = (5, 5, 5, 5)
                        img_enhancer = PIL.ImageEnhance.Brightness(pil_image)
                        factor = 1.1
                        enhanced_output = img_enhancer.enhance(factor)
                        new_resized_im = enhanced_output.resize((int(1.3 * 300), int(1.6 * 300)), PIL.Image.Resampling.LANCZOS)
                        bordered_img = PIL.ImageOps.expand(new_resized_im, border=border, fill=color)
                        resized_image = add_margin(bordered_img, 5, 7, 5, 7, (255, 255, 255))

                        img_list.append(resized_image)
                        img_list.append(resized_image)
                        img_list.append(resized_image)
                        img_list.append(resized_image)
                        img_list.append(resized_image)
                        img_list.append(resized_image)


                pass_photo  = get_multi_pass_photo(img_list,n_rows=(len(image_file)))
                open_cv_image = np.array(pass_photo)
                # Convert RGB to BGR
                open_cv_image = open_cv_image[:, :, ::-1].copy() 
                retval, buffer = cv2.imencode('.jpg', open_cv_image)
                base64_image = base64.b64encode(buffer).decode('utf-8')
                return JsonResponse({'output': base64_image})

        else:
            return JsonResponse({'error': 'No images found.'}, status=400)



def get_multi_pass_photo(im_list, n_rows):
    n_cols = math.ceil(len(im_list) / n_rows)
    width, height = int(8.27 * 300), int(11.7 * 300) # A4 at 300dpi
    # Create a blank A4-sized canvas
    dpi = 300
    a4_width = int(8.27 * dpi)  # A4 width in pixels (8.27 inch at 300 dpi)
    a4_height = int(11.69 * dpi)  # A4 height in pixels (11.69 inch at 300 dpi)
    # a4_sheet = np.ones((a4_height, a4_width, 3), dtype=np.uint8) * 255  # White canvas
    a4_sheet = PIL.Image.new('RGB', (width, height),(255, 255, 255))
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


def add_margin(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = PIL.Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result



