# Generated by Django 3.2.2 on 2021-06-06 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0007_alter_advertisement_memo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='page_id',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
    ]
