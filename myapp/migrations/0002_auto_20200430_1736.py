# Generated by Django 2.1.12 on 2020-04-30 17:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='track',
            name='our_id',
        ),
        migrations.AddField(
            model_name='track',
            name='id',
            field=models.AutoField(auto_created=True, default=0, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='playlist',
            name='tracks',
            field=models.ManyToManyField(to='myapp.Track'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]