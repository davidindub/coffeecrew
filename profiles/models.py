from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from products.models import Product
from checkout.models import Order
from django_countries.fields import CountryField


class WishList(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)
    products = models.ManyToManyField(
        Product, blank=True, related_name='wishlists')

    @property
    def num_products(self):
        return self.products.count()

    def __str__(self):
        return f"{self.user.username}'s Wishlist"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_phone_number = models.CharField(
        max_length=20, null=True, blank=True)
    shipping_address = models.ForeignKey(
        "Address", on_delete=models.SET_NULL,
        null=True, related_name='shipping_address')
    billing_address = models.ForeignKey(
        "Address", on_delete=models.SET_NULL,
        null=True, related_name='billing_address')

    def __str__(self):
        return f"{self.user.username}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        WishList.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    instance.wishlist.save()


class Address(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address_line_1 = models.CharField(max_length=200, null=False)
    address_line_2 = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    postcode = models.CharField(max_length=200, null=False)
    country = CountryField(null=False, blank=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.address_line_1}, {self.city}"
