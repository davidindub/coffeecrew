from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=254)
    visible_to_customers = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=254)
    display_name = models.CharField(max_length=254, null=True, blank=True)
    department = models.ForeignKey(
        "Department", null=True, blank=True, on_delete=models.CASCADE)

    class Meta(object):
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name}"

    def get_display_name(self):
        return f"{self.display_name}"


class Brand(models.Model):
    name = models.CharField(max_length=254)
    display_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    def get_display_name(self):
        return self.display_name


class Product(models.Model):
    slug = models.SlugField(max_length=50, unique=True)
    visible_to_customers = models.BooleanField(default=False)
    name = models.CharField(max_length=254)
    description = models.TextField()
    category = models.ManyToManyField(Category)
    brand = models.ForeignKey(
        "Brand", null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.PositiveSmallIntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"


class Coffee(Product):
    class Meta(object):
        verbose_name_plural = "Coffee"

    COFFEE_BAG_WEIGHTS = (
        ("250g", "250g"),
        ("1kg", "1kg"),
    )
    weight = models.CharField(max_length=24, choices=COFFEE_BAG_WEIGHTS)
    country = models.CharField(max_length=24)
    process = models.CharField(max_length=24)
    harvest_year = models.CharField(max_length=24)


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
