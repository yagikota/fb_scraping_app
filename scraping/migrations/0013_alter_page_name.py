# Generated by Django 3.2.2 on 2021-07-03 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0012_alter_page_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='name',
            field=models.CharField(default='name', max_length=100),
        ),
    ]
