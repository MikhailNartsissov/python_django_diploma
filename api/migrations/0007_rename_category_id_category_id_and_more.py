# Generated by Django 4.2.4 on 2023-08-14 12:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_category_category_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='category_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='subcategory',
            old_name='subcategory_id',
            new_name='id',
        ),
    ]
