# Generated by Django 2.1 on 2018-11-22 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0034_auto_20181119_1727'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='client_google_calendar_added_at',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='client_google_calendar_id',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='stylist_google_calendar_added_at',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='stylist_google_calendar_id',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
    ]
