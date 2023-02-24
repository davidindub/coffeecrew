from django.urls import path
from . import views

urlpatterns = [
    path("", views.DashboardView.as_view(), name="account_dashboard"),
    path('update/', views.ProfileUpdateView.as_view(), name='update_account'),
]
