# Generated by Django 4.1.7 on 2023-05-07 14:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('aiart_content', '0011_comment_imagepostcomment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('report_date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('content', models.TextField(editable=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ImagePostReport',
            fields=[
                ('report_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='aiart_main.report')),
                ('imagepost', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='aiart_content.imagepost')),
            ],
            bases=('aiart_main.report',),
        ),
    ]
