# Generated by Django 4.0.1 on 2023-05-19 19:12

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('coupon_code', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='ProductInventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(max_length=20, unique=True)),
                ('upc', models.CharField(max_length=12, unique=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_default', models.BooleanField(default=False)),
                ('retail_price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('store_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('is_digital', models.BooleanField(default=False)),
                ('weight', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductsOnPromotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promo_price', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('price_override', models.BooleanField(default=False)),
                ('product_inventory', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='promotions_on_product', to='promotion.productinventory')),
            ],
        ),
        migrations.CreateModel(
            name='PromoType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True)),
                ('promo_reduction', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=False)),
                ('is_schedule', models.BooleanField(default=False)),
                ('promo_start', models.DateField()),
                ('promo_end', models.DateField()),
                ('coupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='promotions', to='promotion.coupon')),
                ('products_on_promotion', models.ManyToManyField(related_name='promotions', through='promotion.ProductsOnPromotion', to='promotion.ProductInventory')),
                ('promo_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='promotions', to='promotion.promotype')),
            ],
        ),
        migrations.AddField(
            model_name='productsonpromotion',
            name='promotion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products_on_promotions', to='promotion.promotion'),
        ),
        migrations.AlterUniqueTogether(
            name='productsonpromotion',
            unique_together={('product_inventory', 'promotion')},
        ),
    ]
