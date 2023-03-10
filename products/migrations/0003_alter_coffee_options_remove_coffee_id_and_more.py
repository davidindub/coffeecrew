# Generated by Django 4.1.5 on 2023-01-30 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0002_alter_product_image"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="coffee",
            options={"verbose_name_plural": "Categories"},
        ),
        migrations.RemoveField(
            model_name="coffee",
            name="id",
        ),
        migrations.AddField(
            model_name="coffee",
            name="product_ptr",
            field=models.OneToOneField(
                auto_created=True,
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                parent_link=True,
                primary_key=True,
                serialize=False,
                to="products.product",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="product",
            name="image",
            field=models.ManyToManyField(to="products.image"),
        ),
    ]
