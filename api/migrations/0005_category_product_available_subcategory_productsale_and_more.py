# Generated by Django 4.2.4 on 2023-08-14 11:29

import api.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_review_rate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.CharField(default='1', max_length=3, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=30)),
                ('src', models.ImageField(blank=True, null=True, upload_to=api.models.category_images_directory_path)),
                ('alt', models.CharField(default='There should be an image of the category', max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='available',
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('subcategory_id', models.CharField(default='1.1', max_length=7, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=30)),
                ('src', models.ImageField(blank=True, null=True, upload_to=api.models.category_images_directory_path)),
                ('alt', models.CharField(default='There should be an image of the category', max_length=50)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.category')),
            ],
        ),
        migrations.CreateModel(
            name='ProductSale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salePrice', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('dateFrom', models.DateTimeField()),
                ('dateTo', models.DateTimeField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(default='1.1', on_delete=django.db.models.deletion.PROTECT, to='api.subcategory'),
            preserve_default=False,
        ),
    ]
