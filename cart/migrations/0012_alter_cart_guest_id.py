# Generated by Django 4.1.7 on 2023-03-12 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0011_alter_cart_guest_id_alter_cart_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='guest_id',
            field=models.CharField(blank=True, editable=False, max_length=200, null=True, unique=True),
        ),
    ]