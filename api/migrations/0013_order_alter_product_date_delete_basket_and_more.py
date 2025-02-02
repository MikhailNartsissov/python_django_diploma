# Generated by Django 4.2.4 on 2023-08-18 11:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0012_rename_quantity_basket_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.PositiveSmallIntegerField()),
                ('deliveryType', models.CharField(choices=[('1', 'free'), ('2', 'discount'), ('3', 'standard')], default='3', max_length=1)),
                ('paymentType', models.CharField(choices=[('1', 'card'), ('2', 'cache at an office'), ('3', 'online')], default='3', max_length=1)),
                ('status', models.CharField(choices=[('1', 'basket'), ('2', 'created'), ('3', 'accepted'), ('4', 'in_progress'), ('5', 'payment_accepted'), ('6', 'delivered'), ('7', 'completed')], default='1', max_length=1)),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.DeleteModel(
            name='Basket',
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(related_name='orders', to='api.product'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
