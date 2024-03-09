from django.contrib import admin
from .models import PhotoMaker


class PhotoAdmin(admin.ModelAdmin):
    list_display = ["file"]


admin.site.register(PhotoMaker, PhotoAdmin)

# Register your models here.
