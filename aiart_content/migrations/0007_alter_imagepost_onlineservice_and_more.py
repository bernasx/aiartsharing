# Generated by Django 4.1.7 on 2023-04-06 11:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('aiart_content', '0006_imagepost_remove_post_title_remove_post_views'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagepost',
            name='onlineService',
            field=models.CharField(blank=True, choices=[('DALLE', 'DALL-E 2'), ('NAI', 'Novel AI'), ('MJ', 'Midjourney')], max_length=256),
        ),
        migrations.AlterField(
            model_name='post',
            name='publish_date',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]
