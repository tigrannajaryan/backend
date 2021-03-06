# Generated by Django 2.0.3 on 2018-05-16 09:30

from django.db import migrations, models
import django.db.models.deletion
import salon.types


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_client_uuid'),
        ('salon', '0022_auto_20180510_1311'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=15)),
                ('status', models.CharField(choices=[('unsent', 'Not Sent Yet'), ('delivered', 'Delivered'), ('undelivered', 'Undelivered'), ('accepted', 'Accepted')], default='unsent', max_length=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('delivered_at', models.DateTimeField(default=None, null=True)),
                ('accepted_at', models.DateTimeField(default=None, null=True)),
                ('created_client', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='client.Client')),
                ('stylist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salon.Stylist')),
            ],
            options={
                'db_table': 'invitation',
            },
        ),
    ]
