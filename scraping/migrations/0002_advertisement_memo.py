# Generated by Django 3.2.2 on 2021-05-23 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='memo',
            field=models.TextField(max_length=500, null=True),
        ),
    ]
