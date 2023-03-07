from django.urls import path
from .views import (ProductsListView, product_detail)

urlpatterns = [
    path("", ProductsListView.as_view(), name="products"),
    path("c/<category>/",
         ProductsListView.as_view(), name="products_by_category"),
    path("d/<department>/",
         ProductsListView.as_view(), name="products_by_department"),
    path("b/<brand>/",
         ProductsListView.as_view(), name="products_by_brand"),
    path("item/<slug:slug>", product_detail, name="product_detail")
]
