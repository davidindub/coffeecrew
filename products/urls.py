from django.urls import path
from .views import (ProductsList, ProductUpdate, CoffeeUpdate,
                    product_detail, ProductCreate)

urlpatterns = [
    path("", ProductsList.as_view(), name="products"),
    path("c/<category>/",
         ProductsList.as_view(), name="products_by_category"),
    path("d/<department>/",
         ProductsList.as_view(), name="products_by_department"),
    path("item/<slug:slug>", product_detail, name="product_detail"),
    path('item/<slug:slug>/update/',
         ProductUpdate.as_view(), name='product_update'),
    path('coffee/<slug:slug>/update/',
         CoffeeUpdate.as_view(), name='coffee_update'),
    path('staff/new/product', ProductCreate.as_view(), name='product_create'),
]
