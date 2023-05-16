from django.urls import path

from .views import get_emails

urlpatterns = [
    path("", get_emails, name="get-emails"),
]
