from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from products.models import Product, Coffee
from coffeecrew import settings
from decimal import Decimal
from cart.cart_logic import (calculate_delivery_cost,
                             calculate_total_with_delivery,
                             get_spend_for_free_delivery,
                             is_free_delivery)


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                null=True, blank=True, editable=False)
    guest_id = models.CharField(
        max_length=100, null=True, blank=True, unique=True, editable=False)
    updated = models.DateTimeField(auto_now=True)

    @property
    def item_count(self):
        return sum(item.quantity for item in self.cart_item.all())

    def total(self):
        return Decimal(sum(item.total() for item in self.cart_item.all()))

    def __str__(self):
        if self.user:
            return f"User {self.user.username}'s Cart"
        else:
            return f"Guest Cart ID last updated { self.updated }"

    @property
    def delivery_total(self):
        return calculate_delivery_cost(self.total())

    @property
    def free_delivery(self):
        return is_free_delivery(self.total())

    @property
    def spend_for_free_delivery(self):
        return get_spend_for_free_delivery(self.total())

    @property
    def total_with_delivery(self):
        return calculate_total_with_delivery(self.total())

    def empty_cart(self):
        """
        Empty all the cart items
        """
        self.cart_item.all().delete()

    def reset_cart_after_sale(self):
        """
        Empty the cart items and clear the stripe payment intent
        """
        self.empty_cart()
        self.stripe_payment_intent = None


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="cart_item")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    grind_size = models.CharField(
        max_length=50,
        choices=[
            ("Wholebean", "Wholebean"),
            ("Moka Pot", "Moka Pot"),
            ("French Press", "French Press"),
            ("Pour Over", "Pour Over"),
            ("Filter/Drip", "Filter/Drip"),
            ("Espresso", "Espresso")
        ],
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        try:
            coffee = self.product.coffee
        except Coffee.DoesNotExist:
            coffee = None

        if coffee:
            self.grind_size = self.grind_size or "Wholebean"
        else:
            self.grind_size = None

        super().save(*args, **kwargs)

    def adjust_quantity(self, quantity):
        self.quantity = quantity
        if self.quantity == 0:
            self.delete()
            return True
        if self.quantity <= self.product.stock:
            self.save()
            return True
        else:
            return False

    def total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


@receiver(post_save, sender=User)
def create_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_cart(sender, instance, **kwargs):
    instance.cart.save()
