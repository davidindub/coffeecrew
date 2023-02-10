from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from products.models import Product


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)

    @property
    def item_count(self):
        return sum(item.quantity for item in self.cartitem_set.all())

    def total(self):
        return sum(item.total() for item in self.cartitem_set.all())

    def __str__(self):
        return f"{self.user.username}'s Cart"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='cartitem_set')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

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