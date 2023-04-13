# Generated by Django 4.1.5 on 2023-01-29 18:44

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('aiart_content', '0002_post_uuid_post_views'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('1808256c-379c-415d-abbf-ba5d5285dee9'), editable=False, unique=True),
        ),
    ]