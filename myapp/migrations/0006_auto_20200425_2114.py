# Generated by Django 2.1.12 on 2020-04-25 21:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_auto_20200425_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='users',
            field=models.ManyToManyField(blank=True, default=None, to=settings.AUTH_USER_MODEL),
        ),
    ]
