# Generated by Django 2.1 on 2018-10-11 16:46

from django.db import migrations


def populate_client_field(apps, schema_editor):
    Invitation = apps.get_model('salon', 'Invitation')
    Client = apps.get_model('client', 'Client')
    for invitation in Invitation.objects.filter(
            created_client__isnull=True, created_real_client__isnull=False).iterator():
        client: Client = invitation.created_real_client
        invitation.created_client = client
        invitation.save(update_fields=['created_client', ])


class Migration(migrations.Migration):

    dependencies = [
        ('salon', '0057_auto_20181011_1158'),
    ]

    operations = [
        migrations.RunPython(populate_client_field, migrations.RunPython.noop)
    ]