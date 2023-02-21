# Generated by Django 4.1.7 on 2023-02-21 16:11

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
        ('profiles', '0003_alter_wishlist_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='default_county',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='default_postcode',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='default_street_address1',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='default_street_address2',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='default_town_or_city',
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_line_1', models.CharField(max_length=200)),
                ('address_line_2', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('postcode', models.CharField(max_length=200)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='checkout.order')),
                ('profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='profiles.profile')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='billing_address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='billing_address', to='profiles.address'),
        ),
        migrations.AddField(
            model_name='profile',
            name='shipping_address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shipping_address', to='profiles.address'),
        ),
    ]