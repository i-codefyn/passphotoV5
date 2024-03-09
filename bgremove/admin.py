from django.contrib import admin

from .models import BgRemove


@admin.register(BgRemove)
class BgRemoveAdmin(admin.ModelAdmin):
    list_display = ["image", "output", "created_at"]
