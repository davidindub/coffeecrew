# Generated by Django 4.1.7 on 2023-02-24 17:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_remove_profile_default_county_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='order',
        ),
    ]
