# Generated by Django 4.2.4 on 2023-09-06 13:11

import api.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0033_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullName', models.CharField(max_length=80)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.PositiveSmallIntegerField()),
                ('src', models.ImageField(blank=True, null=True, upload_to=api.models.avatar_images_directory_path)),
                ('alt', models.CharField(default='There should be an image of the product', max_length=50)),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.profile')),
            ],
        ),
    ]