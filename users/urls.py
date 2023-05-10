from django.urls import path

from .views import (
    SupportView,
    TemplateCreateView,
    TemplateUpdateView,
    UserSettingsView,
    create_checkout_session,
    create_customer_portal_session,
    resend_email_confirmation_email,
)

urlpatterns = [
    path("settings/", UserSettingsView.as_view(), name="settings"),
    path("create-checkout-session", create_checkout_session, name="upgrade-user"),
    path("support", SupportView.as_view(), name="support"),
    path("templates", TemplateCreateView.as_view(), name="templates"),
    path(
        "template/<uuid:pk>/update",
        TemplateUpdateView.as_view(),
        name="update-template",
    ),
    path(
        "create-customer-portal-session/",
        create_customer_portal_session,
        name="create-customer-portal-session",
    ),
    path(
        "send-confirmation",
        resend_email_confirmation_email,
        name="resend_email_confirmation_email",
    ),
]
