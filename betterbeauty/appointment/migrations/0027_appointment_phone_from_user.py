# Generated by Django 2.1 on 2018-09-30 13:49
from django.contrib.gis.db.backends.postgis.schema import PostGISSchemaEditor
from django.db import migrations
from django.db.migrations.state import StateApps


def copy_user_phone_in_appointment(apps: StateApps, schema_editor: PostGISSchemaEditor):
    Appointment = apps.get_model('appointment', 'Appointment')
    appointments = Appointment.objects.exclude(client_id=None)
    for appointment in appointments:
        if appointment.client.client and not appointment.client_phone:
            appointment.client_phone = appointment.client.client.user.phone
            appointment.save()


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0026_auto_20180904_0914'),
    ]

    operations = [
        migrations.RunPython(code=copy_user_phone_in_appointment, reverse_code=migrations.RunPython.noop)
    ]