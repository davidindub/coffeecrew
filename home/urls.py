from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("about", views.about, name="about"),
    path("privacy", views.privacy_policy, name="privacy"),
    path("contact", views.contact_us, name="contact"),
    ]
