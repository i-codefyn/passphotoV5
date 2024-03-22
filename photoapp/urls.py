from django.urls import path
from photoapp import views

app_name = "photoapp"

urlpatterns = [
    path("", views.PassPhotosCreaterView.as_view(), name="home"),
    path("bg_remove/", views.BgRemoveView.as_view(), name="bg_remove"),

]
