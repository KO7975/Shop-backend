# Generated by Django 4.2.2 on 2023-06-29 09:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0010_productattribute_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='reserved_quantity',
            field=models.IntegerField(null=True),
        ),
        # migrations.AlterField(
        #     model_name='comment',
        #     name='dislikes',
        #     field=models.ManyToManyField(blank=True, related_name='comment_dislikes', through='product.CommentDislike', to=settings.AUTH_USER_MODEL),
        # ),
        # migrations.AlterField(
        #     model_name='comment',
        #     name='likes',
        #     field=models.ManyToManyField(blank=True, related_name='comment_likes', through='product.CommentLike', to=settings.AUTH_USER_MODEL),
        # ),
    ]