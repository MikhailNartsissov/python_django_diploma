# Generated by Django 4.2.4 on 2023-09-17 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0038_tag_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profileimage',
            name='alt',
            field=models.CharField(default='There should be an image of the profile', max_length=50),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='alt',
            field=models.CharField(default='There should be an image of the subcategory', max_length=50),
        ),
    ]
