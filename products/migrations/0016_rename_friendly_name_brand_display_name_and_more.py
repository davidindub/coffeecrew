# Generated by Django 4.1.5 on 2023-02-16 16:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_rename_display_name_brand_friendly_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='brand',
            old_name='friendly_name',
            new_name='display_name',
        ),
        migrations.RenameField(
            model_name='category',
            old_name='friendly_name',
            new_name='display_name',
        ),
    ]
