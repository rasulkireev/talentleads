from django.urls import path

from .views import HomeView, PricingView, ProductHuntView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("product-hunt", ProductHuntView.as_view(), name="product-hunt"),
    path("pricing", PricingView.as_view(), name="pricing"),
]
