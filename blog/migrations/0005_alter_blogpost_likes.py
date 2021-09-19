# Generated by Django 3.2.7 on 2021-09-17 09:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0004_alter_blogpost_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='blog_post', to=settings.AUTH_USER_MODEL),
        ),
    ]
