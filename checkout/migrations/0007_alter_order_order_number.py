# Generated by Django 4.1.7 on 2023-03-05 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0006_orderlineitem_order_full_name_delete_orderitem_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
