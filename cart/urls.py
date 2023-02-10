from django.urls import path
from .views import CartView, CartAddView, CartRemoveView

urlpatterns = [
    path('', CartView.as_view(), name='shopping_cart'),
    path('add/<int:product_id>/', CartAddView.as_view(), name='cart_add'),
    path('remove/<int:product_id>/',
         CartRemoveView.as_view(), name='cart_remove'),
]
