# Generated by Django 4.2.4 on 2023-09-04 15:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0032_rename_delivery_type_order_deliverytype_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('number', models.CharField(max_length=20)),
                ('month', models.CharField(max_length=2)),
                ('year', models.CharField(max_length=4)),
                ('code', models.CharField(max_length=3)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.order')),
            ],
        ),
    ]
