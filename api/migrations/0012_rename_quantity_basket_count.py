# Generated by Django 4.2.4 on 2023-08-17 08:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_basket'),
    ]

    operations = [
        migrations.RenameField(
            model_name='basket',
            old_name='quantity',
            new_name='count',
        ),
    ]
