# Generated by Django 3.2.2 on 2021-06-06 12:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0004_auto_20210529_1639'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='scraped_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
