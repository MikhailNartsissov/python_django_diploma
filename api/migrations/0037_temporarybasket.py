# Generated by Django 4.2.4 on 2023-09-16 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0036_alter_order_address_alter_order_city_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TemporaryBasket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session', models.CharField(max_length=32)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('count', models.DecimalField(decimal_places=0, max_digits=6)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_tmp', to='api.product')),
            ],
        ),
    ]