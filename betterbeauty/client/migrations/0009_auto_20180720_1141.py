# Generated by Django 2.0.3 on 2018-07-20 15:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0008_auto_20180709_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preferredstylist',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='preferred_stylists', to='client.Client'),
        ),
    ]
