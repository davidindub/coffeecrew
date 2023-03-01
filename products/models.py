from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=254)
    visible_to_customers = models.BooleanField(default=False)

    @property
    def num_products(self):
        categories = self.category_set.all()
        num_products = sum([category.num_products for category in categories])
        return num_products

    @property
    def num_categories(self):
        return self.category_set.count()

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

    @property
    def num_products(self):
        return self.product_set.count()


class Brand(models.Model):
    name = models.CharField(max_length=254)
    display_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    @property
    def num_products(self):
        return self.product_set.count()


class Product(models.Model):
    visible_to_customers = models.BooleanField(default=False)
    name = models.CharField(max_length=254)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    category = models.ManyToManyField(Category)
    brand = models.ForeignKey(
        "Brand", null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True,
                           blank=True, unique=True, editable=False)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.PositiveSmallIntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(
        upload_to='product_images/', blank=True, null=True)
    lifetime_sales = models.PositiveSmallIntegerField(
        default=0, editable=False)

    def save(self, *args, **kwargs):
        # update the slug if the name is changed
        if self.pk:
            original_name = Product.objects.get(pk=self.pk).name
            if original_name != self.name:
                self.slug = slugify(self.name)

        # generate a new slug if none exists
        if not self.slug:
            self.slug = slugify(self.name)

        super(Product, self).save(*args, **kwargs)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except AttributeError:
            url = ""
        return url

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
