from django.conf.urls import url
from .views import save_device, send_notification

app_name = "notifications"


urlpatterns = [
    url(r"send/$", send_notification, name="send"),
    url(r"save/$", save_device, name="save"),
]