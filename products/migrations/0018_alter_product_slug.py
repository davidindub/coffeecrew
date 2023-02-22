# Generated by Django 4.1.7 on 2023-02-22 13:30

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_product_image_delete_productimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=autoslug.fields.AutoSlugField(
                editable=False, populate_from='name', unique=True),
        ),
    ]
