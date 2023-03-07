from django.urls import path
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="home"),
    path("about", views.AboutView.as_view(), name="about"),
    path("privacy", views.PrivacyPolicyView.as_view(), name="privacy"),
    path("contact", views.ContactUsView.as_view(), name="contact"),
    ]
