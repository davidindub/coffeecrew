# Generated by Django 4.1.5 on 2023-02-16 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_department_category_department'),
    ]

    operations = [
        migrations.RenameField(
            model_name='brand',
            old_name='display_name',
            new_name='friendly_name',
        ),
        migrations.RenameField(
            model_name='category',
            old_name='display_name',
            new_name='friendly_name',
        ),
        migrations.RemoveField(
            model_name='product',
            name='wish_lists',
        ),
    ]
