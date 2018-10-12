# Generated by Django 2.1 on 2018-09-26 11:52
import phonenumbers
from django.contrib.gis.db.backends.postgis.schema import PostGISSchemaEditor

from django.db import migrations
from django.db.migrations.state import StateApps

from api.v1.auth.utils import get_country_code_from_phone


def set_country_from_phone(apps: StateApps, schema_editor: PostGISSchemaEditor):
    Client = apps.get_model('client', 'Client')
    clients = Client.objects.filter(country=None)
    for client in clients:
        client.country = get_country_code_from_phone(client.user.phone)
        client.save()


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0017_auto_20180926_0751'),
    ]

    operations = [
        migrations.RunPython(code=set_country_from_phone, reverse_code=migrations.RunPython.noop)
    ]