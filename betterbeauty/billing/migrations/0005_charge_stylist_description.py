# Generated by Django 2.1 on 2019-02-22 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0004_auto_20190215_0853'),
    ]

    operations = [
        migrations.AddField(
            model_name='charge',
            name='stylist_description',
            field=models.TextField(blank=True, null=True),
        ),
    ]