# Generated by Django 2.1 on 2019-02-22 15:42

import django.contrib.postgres.fields.jsonb
from django.db import migrations
import notifications.models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0014_notification_sms_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='email_details',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=notifications.models.default_json_field_value, null=True),
        ),
    ]
