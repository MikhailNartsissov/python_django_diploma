# Generated by Django 4.2.4 on 2023-09-01 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0030_order_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_type',
            field=models.CharField(default='ordinary', max_length=30),
        ),
    ]