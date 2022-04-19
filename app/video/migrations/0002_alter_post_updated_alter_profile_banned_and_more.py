# Generated by Django 4.0.3 on 2022-04-18 13:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('video', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='banned',
            field=models.ManyToManyField(blank=True, null=True, related_name='bans', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profile',
            name='ignored',
            field=models.ManyToManyField(blank=True, null=True, related_name='ignores', to=settings.AUTH_USER_MODEL),
        ),
    ]
