# Generated by Django 4.2.4 on 2023-08-14 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_category_product_available_subcategory_productsale_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_id',
            field=models.DecimalField(decimal_places=0, default=1, max_digits=3, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='subcategory_id',
            field=models.DecimalField(decimal_places=0, default=1001, max_digits=6, primary_key=True, serialize=False, unique=True),
        ),
    ]