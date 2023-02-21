from django.urls import path
from .views import ProductsList, ProductUpdate, product_detail

urlpatterns = [
    path("", ProductsList.as_view(), name="products"),
    path("c/<category>/",
         ProductsList.as_view(), name="products_by_category"),
    path("d/<department>/",
         ProductsList.as_view(), name="products_by_department"),
    path("item/<product_id>", product_detail, name="product_detail"),
    path('item/<slug:slug>/update/',
         ProductUpdate.as_view(), name='product_update'),
]
