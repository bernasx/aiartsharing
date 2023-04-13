# Generated by Django 4.1.5 on 2023-01-29 18:47

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('aiart_content', '0004_alter_post_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]