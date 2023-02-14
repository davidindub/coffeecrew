from django.urls import path
from . import views

urlpatterns = [
    path("", views.ProductsList.as_view(), name="products"),
    path("c/<category>/",
         views.ProductsList.as_view(), name="products_by_category"),
    path("d/<department>/",
         views.ProductsList.as_view(), name="products_by_department"),
    path("item/<product_id>", views.product_detail, name="product_detail"),
]
