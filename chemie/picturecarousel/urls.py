from django.urls import path

from . import views

app_name = "picturecarousel"

urlpatterns = [
    path("", views.submit_picture, name="submit"),
    path("karusell", views.view_carousel, name="display"),
    path("godkjenn/", views.approve_pictures, name="overview"),
    path(
        "godkjenn/approve/<int:picture_id>", views.approve_deny, name="approve"
    ),
    path(
        "godkjenn/deny/<int:picture_id>",
        views.approve_deny,
        {"deny": True},
        name="deny",
    ),
    path("aktive/", views.view_pictures, name="view_pictures"),
    path("tagg/<int:id>", views.tag_users, name="tag_users"),
]
