from django.urls import path

from . import views

app_name = "bgremove"

urlpatterns = [
   
    path("bg/", views.ProgressBarUploadView.as_view(), name="bg"),
    # path("", views.ProgressBarUploadView.as_view(), name="index"),
    path("", views.UploadView.as_view(), name="index"),
    # path("upload/", upload, name="upload"),
    # path("output/list", OutputListView1.as_view(), name="output_list"),
    path("output/list", views.OutputListView.as_view(), name="output_list"),
    path("output/<uuid:pk>", views.OutputView.as_view(), name="output"),
    path("output/<uuid:pk>/download", views.download_file, name="download"),
    path("output/<uuid:pk>/delete", views.FileDeleteView.as_view(), name="delete"),
]
