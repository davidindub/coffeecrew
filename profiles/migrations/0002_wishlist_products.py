# Generated by Django 4.1.5 on 2023-02-16 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_rename_display_name_brand_friendly_name_and_more'),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishlist',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='wishlists', to='products.product'),
        ),
    ]
