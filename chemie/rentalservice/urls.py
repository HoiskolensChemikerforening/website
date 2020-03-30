from . import views
from django.urls import path

app_name = "rentalservice"

urlpatterns = [path("", views.index, name="index"),
               path("ny", views.new_object, name="new_object")]

