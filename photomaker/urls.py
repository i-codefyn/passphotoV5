from django.urls import path
from photomaker import views

app_name = "photo"
urlpatterns = [
    path("", views.HomeView.as_view(), name="index"),
    path("terms_and_conditions/", views.Terms.as_view(), name="terms"),
    path("privacy/", views.Privacy.as_view(), name="privacy"),
    path("passphoto/", views.PhotosCreateView.as_view(), name="pass_photo"),
    # path(
    #     "pass_photo/multi_photo",
    #     views.MultiPhoto.as_view(),
    #     name="multi_photo",
    # ),
    path(
        "pass_photo/output_list/",
        views.PhotosOutputList.as_view(),
        name="pass_photo_list",
    ),
   
    path("pass_photo/<uuid:pk>", views.PassPhoto.as_view(), name="photos"),
    path("pass_photo/<uuid:pk>/one", views.pass_photo_single),
    path("pass_photo/<uuid:pk>/4by6", views.pass_photo_full_4by6),
    path("pass_photo/<uuid:pk>/6", views.pass_photo_6),
    path("pass_photo/<uuid:pk>/12", views.pass_photo_12),
    path("pass_photo/<uuid:pk>/18", views.pass_photo_18),
    path("pass_photo/<uuid:pk>/24", views.pass_photo_24),
    path("pass_photo/<uuid:pk>/30", views.pass_photo_30),
    path("pass_photo/<uuid:pk>/36", views.pass_photo_36),
    path("pass_photo/<uuid:pk>/full",views.pass_photo_full),
    path("pass_photo/<uuid:pk>/delete",views.FileDeleteView.as_view(), name="delete"),
    path("pass_photo/<uuid:pk>/pdf", views.pass_photo_6, name="photos_list"),
    # path("img/<uuid:pk>/", views.pass_photo_6, name="photos"),
    # path("staff/Works/<uuid:pk>", WorkDetails.as_view(), name="work_sheet"),
    # path("", UploadView.as_view(), name="home"),
    # path("output/<uuid:pk>/", OutputView.as_view(), name="output"),
]
