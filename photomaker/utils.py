from django.conf import settings

# Path
from pathlib import Path

# template rendering
from django.template import loader
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# QR CODE
import io
import time
import datetime

# PDF
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os


import base64
def fetch_resources(uri, rel):
    path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    return path


def ShowPDF(template_src, context_dict={}, pdf_name={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    
    
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{pdf_name}"'
    pdf_file = pisa.CreatePDF(
        html.encode("ISO-8859-1"), dest=response, link_callback=fetch_resources
    )

    return response


def RenderToPDF(template_src, context_dict={}, pdf_name={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{pdf_name}"'
    with open(pdf_name, "wb+") as output:
        pdf = pisa.pisaDocument(
            io.BytesIO(html.encode("UTF-8")), output, link_callback=fetch_resources
        )
    return output.name
