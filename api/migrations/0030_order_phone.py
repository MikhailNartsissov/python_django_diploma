# Generated by Django 4.2.4 on 2023-09-01 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0029_remove_order_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
