# Generated by Django 2.1 on 2018-10-30 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0063_auto_20181031_1409'),
        ('core', '0035_auto_20181018_1218'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stylist',
            name='rebook_within_5_weeks_discount_percent',
        ),
        migrations.RemoveField(
            model_name='stylist',
            name='rebook_within_6_weeks_discount_percent',
        ),
    ]
