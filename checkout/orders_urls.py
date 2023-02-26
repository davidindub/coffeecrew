from django.urls import path
from .views import OrderDetailView, StaffOrderListView

urlpatterns = [
    path("detail/<str:order_number>/", OrderDetailView.as_view(), name="order_detail"),
    path("staff/", StaffOrderListView.as_view(), name="manage_orders"),
]
