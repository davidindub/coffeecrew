from django.db import models
from django_countries.fields import CountryField


class SiteSettings(models.Model):
    """
    Site settings for the owner to change in the frontend
    """
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2)
    min_free_delivery_spend = models.DecimalField(
        max_digits=6, decimal_places=2)
    currency_symbol = models.CharField()


class DeliveryOption(models.Model):
    """
    Model to represent a delivery option
    """
    name = models.CharField(max_length=255)
    active = models.BooleanField()
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    free_with_spend_over = models.DecimalField(
        max_digits=6, decimal_places=2)
    countries = CountryField(multiple=True)

    def __str__(self):
        return f"{self.name} ({self.cost})"
