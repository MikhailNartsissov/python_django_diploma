# Generated by Django 4.2.4 on 2023-08-21 17:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_order_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
