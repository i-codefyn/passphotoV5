# Even better as it works in any browser (mobile and desktop)
def safe_name(file_name):
    """
    Generates a safe file name, even those containing characters like ? and &
    And your Kanji and Cyrillics are supported!
    """
    u_file_name = file_name.encode('utf-8')
    s_file_name = re.sub('[\x00-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), u_file_name)
    return s_file_name

# Handled by url(r'^/image/download/(\d+)/.+$
def safe_download_image(request, image_id):
    """
    Safely downloads the file because the filename is part of the URL
    """
    img = ImageModel.objects.get(id=image_id)
    wrapper      = FileWrapper(open(img.file))  # img.file returns full path to the image
    content_type = mimetypes.guess_type(filename)[0]  # Use mimetypes to get file type
    response     = HttpResponse(wrapper,content_type=content_type)
    response['Content-Length']      = os.path.getsize(img.file)
    # This works for most browsers, but IE will complain sometimes
    response['Content-Disposition'] = "attachment;"
    return response

def download_image(request, image_id):
    img = ImageModel.objects.get(id=image_id)
    redirect_do = safe_name(img.name)
    return HttpResponseRedirect('/image/download/' + img_id + '/' + redirect_to)