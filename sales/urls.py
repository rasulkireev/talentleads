from django.urls import path

from .views import send_marketing_emails

urlpatterns = [
    path("", send_marketing_emails, name="send-marketing-emails"),
]
