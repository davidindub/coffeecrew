from django.urls import path
from products.views import ProductsList
from .views import AddToWishlistView, RemoveFromWishlistView

urlpatterns = [
    path("", ProductsList.as_view(),
         kwargs={"wishlist": True}, name="wish_list"),
    path("add/<int:product_id>/",
         AddToWishlistView.as_view(), name="add_to_wishlist"),
    path("remove/<int:product_id>/",
         RemoveFromWishlistView.as_view(), name="remove_from_wishlist"),
]
