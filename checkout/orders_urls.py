from django.urls import path
from .views import OrderDetailView, OrderDispatchView, StaffOrderListView

urlpatterns = [
    path("detail/<str:order_number>/",
         OrderDetailView.as_view(), name="order_detail"),
    path("detail/<str:order_number>/dispatch",
         OrderDispatchView.as_view(), name="order_dispatched"),
    path("staff/", StaffOrderListView.as_view(), name="manage_orders"),
]
