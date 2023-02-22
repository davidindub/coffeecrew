from django.urls import path
from .views import (ProductsList, ProductUpdate,
                    CoffeeUpdate, DepartmentCreate, DepartmentDelete,
                    DepartmentUpdate, ManageCategories, product_detail,
                    ProductCreate)

urlpatterns = [
    path("", ProductsList.as_view(), name="products"),
    path("c/<category>/",
         ProductsList.as_view(), name="products_by_category"),
    path("d/<department>/",
         ProductsList.as_view(), name="products_by_department"),
    path("item/<slug:slug>", product_detail, name="product_detail"),
    path("item/<slug:slug>/update/",
         ProductUpdate.as_view(), name="product_update"),
    path("coffee/<slug:slug>/update/",
         CoffeeUpdate.as_view(), name="coffee_update"),
    path("staff/new/product", ProductCreate.as_view(), name="product_create"),
    path("staff/department/new/", DepartmentCreate.as_view(),
         name="department_create"),
    path("staff/department/<int:pk>/delete/",
         DepartmentDelete.as_view(), name="department_delete"),
    path("staff/department/<int:pk>/update/", DepartmentUpdate.as_view(),
         name="department_update"),
    path("staff/", ManageCategories.as_view(),
         name="manage_categories")
]
