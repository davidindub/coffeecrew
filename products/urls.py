from django.urls import path
from . import views

urlpatterns = [
    path("", views.ProductsList.as_view(), name="products"),
    path("<category>/",
         views.ProductsList.as_view(), name="products_by_category"),
    path("<product_id>", views.product_detail, name="product_detail"),
]
