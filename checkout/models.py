from django.contrib.auth.models import User
from coffeecrew.settings import FREE_DELIVERY_THRESHOLD, DELIVERY_COST
from django.db import models, IntegrityError
from django_countries.fields import CountryField
from products.models import Product
from django.dispatch import receiver
from django.db.models.signals import post_save
import datetime
import random


class Order(models.Model):
    """
    Represents Customer Orders
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)
    order_number = models.CharField(max_length=15, unique=True)
    delivery_method = models.CharField(max_length=20, null=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2,
                                        null=False, default=DELIVERY_COST)
    order_total = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=False, default=0)
    stripe_pid = models.CharField(max_length=254, null=False, blank=False,
                                  default='')
    full_name = models.CharField(max_length=200, null=True)
    address_line_1 = models.CharField(max_length=200, null=False)
    address_line_2 = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    postcode = models.CharField(max_length=200, null=False)
    country = CountryField(null=False, blank=False)
    shipped_date = models.DateTimeField(null=True, blank=True)

    def generate_order_number(self):
        """
        Generate an Order Number representing the
        month, year and 8 random digits.
        e.g. FEB210674310, MAR210201623
        """
        now = datetime.datetime.now()
        month = now.strftime("%b").upper()
        day = now.strftime("%d")
        random_digits = "".join(random.choice("0123456789") for _ in range(8))
        return f"{month}{day}{random_digits}"

    def update_totals(self):
        """
        Update order_total to the total of all OrderItems
        """
        order_items = self.order_items.all()
        total = sum([item.price for item in order_items])
        self.order_total = total
        self.grand_total = self.order_total + self.delivery_cost

    def set_as_shipped(self):
        """
        Set the Shipped Date and set order as complete
        """
        self.shipped_date = datetime.datetime.now()
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already. If not unique, generate a new one and
        try to save again.
        Update the order total & grand total
        """
        if not self.order_number:
            self.order_number = self.generate_order_number()

        while True:
            try:
                # self.update_totals()
                super().save(*args, **kwargs)
                break
            except IntegrityError:
                self.order_number = self.generate_order_number()

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    """
    Represents a product in an order. The price is locked in at
    at the time of the orders creation as the price may change in future.
    """
    order = models.ForeignKey(Order, null=False, blank=False,
                              on_delete=models.CASCADE,
                              related_name="order_items")
    product = models.ForeignKey(
        Product, null=False, blank=False,
        on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    grind_size = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    price = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True, editable=False)
    product_name = models.CharField(
        max_length=254, null=True, blank=True, editable=False)
    total = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True, editable=False)

    def set_details(self):
        if not self.price:
            self.price = self.product.price
        if not self.product_name:
            self.product_name = self.product.name
        self.total = self.product.price * self.quantity

    def save(self, *args, **kwargs):
        """
        Set the price if it hasn't been already set.
        Save the product's name in case it becomes unavailable on the site,
        so not to break users order history.
        """
        self.set_details()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"


@receiver(post_save, sender=OrderLineItem)
def lock_price(sender, instance, created, **kwargs):
    if created:
        instance.set_details()
        instance.save()
