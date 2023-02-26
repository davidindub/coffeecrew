from django.urls import path
from .views import OrderDetailView

urlpatterns = [
    path('<str:order_number>/', OrderDetailView.as_view(), name='order_detail'),
]
