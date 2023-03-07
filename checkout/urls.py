from django.urls import path, include
from .views import (CheckoutReviewView, CheckOutShippingView,
                    CheckoutPaymentView, SuccessView, CancelView,
                    PaymentFailedView)

urlpatterns = [
    path("", CheckoutReviewView.as_view(), name="checkout"),
    path("delivery/", CheckOutShippingView.as_view(),
         name="checkout_delivery"),
    path("payment/", CheckoutPaymentView.as_view(),
         name="checkout_payment"),
    path("cancel/", CancelView.as_view(), name="cancel"),
    path("success/", SuccessView.as_view(), name="payment_success"),
    path("payment/failure/", PaymentFailedView.as_view(),
         name="payment_failure"),
]
