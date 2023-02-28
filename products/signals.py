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
        last_sku_number = Product.objects.order_by('-id').first().id + 1
        sku = f"{brand_name}{last_sku_number:04}"
        while Product.objects.filter(sku=sku).exists():
            last_sku_number += 1
            sku = f"{brand_name}{last_sku_number:04}"
        instance.sku = sku