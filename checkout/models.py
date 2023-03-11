from django.contrib.auth.models import User
from coffeecrew.settings import FREE_DELIVERY_THRESHOLD, DELIVERY_COST
from django.db import models, IntegrityError
from django_countries.fields import CountryField
from products.models import Product
from django.dispatch import receiver
from django.db.models.signals import post_save
import datetime
from django.utils import timezone
import random


class Order(models.Model):
    """
    Represents Customer Orders
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)
    order_placed_date = models.DateTimeField(null=True, blank=True,
                                             editable=False)
    order_number = models.CharField(max_length=15, unique=True)
    delivery_method = models.CharField(max_length=20, null=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2,
                                        null=False, default=0.00)
    stripe_pid = models.CharField(max_length=254, null=False, blank=False,
                                  default='')
    full_name = models.CharField(max_length=200, null=True)
    address_line_1 = models.CharField(max_length=200, null=False)
    address_line_2 = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    postcode = models.CharField(max_length=200, null=False)
    country = CountryField(null=False, blank=False)
    shipped_date = models.DateTimeField(null=True, blank=True)

    @property
    def order_total(self):
        line_items = self.order_items.all()
        return sum([item.total for item in line_items])

    @property
    def grand_total(self):
        order_total = self.order_total
        return self.order_total + self.delivery_cost

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

    def set_as_shipped(self):
        """
        Set the Shipped Date and set order as complete
        """
        self.shipped_date = datetime.datetime.now(tz=timezone.utc)
        self.save()

    def complete_order(self):
        """
        Set order as complete, decrement product stock
        """
        self.completed = True
        self.order_placed_date = datetime.datetime.now(tz=timezone.utc)

        for item in self.order_items.all():
            quantity = item.quantity
            item.product.make_sale(quantity)

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
                    super().save(*args, **kwargs)
                    break
                except IntegrityError:
                    print(f"Duplicate order number")
                    # Catch potential duplicate order numbers and
                    #  generate new order number
                    self.order_number = self.generate_order_number()
                except ValueError:
                    print("Can't update totals until order created")
        else:
            super().save(*args, **kwargs)

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
        max_digits=6, decimal_places=2, null=True, blank=True)
    product_name = models.CharField(
        max_length=254, null=True, blank=True, editable=False)

    @property
    def total(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
