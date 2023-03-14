from django.urls import path
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="home"),
    path("newsletter", views.NewsletterView.as_view(), name="newsletter"),
    path("privacy", views.PrivacyPolicyView.as_view(), name="privacy"),
    path("contact", views.ContactUsView.as_view(), name="contact"),
    path("contact/submit", views.ContactUsSuccessView.as_view(),
         name="contact_submit"),
]
