import random
import string
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Product


@receiver(pre_save, sender=Product)
def create_sku(sender, instance, **kwargs):
    """
    Create a SKU based on the brand name,
    if no brand use 'CCC'
    """
    if not instance.sku:
        if instance.brand:
            brand_name = instance.brand.name[:3].upper()
        else:
            brand_name = "CCC"
        while True:
            digits = string.digits
            sku_number = "".join(random.choice(digits) for i in range(5))
            sku = f"{brand_name}{sku_number}"
            if not Product.objects.filter(sku=sku).exists():
                instance.sku = sku
                break
