# Generated by Django 4.1.7 on 2023-04-26 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aiart_content', '0010_alter_imagepost_onlineservice'),
        ('aiart_auth', '0009_customuser_profile_picture_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='liked_image_posts',
            field=models.ManyToManyField(related_name='liked_image_posts', to='aiart_content.imagepost'),
        ),
    ]