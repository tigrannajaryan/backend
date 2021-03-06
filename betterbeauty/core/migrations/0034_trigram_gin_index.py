# Generated by Django 2.1 on 2018-10-12 12:59

from django.db import migrations


class Migration(migrations.Migration):
    atomic = False # disable transaction for creating concurrent indexes

    dependencies = [
        ('core', '0033_install_trigram_extension'),
    ]

    operations = [
        migrations.RunSQL(
            'CREATE INDEX CONCURRENTLY "salon_name_gin_idx" ON "salon" USING GIN(name gin_trgm_ops);',
            reverse_sql='DROP INDEX CONCURRENTLY IF EXISTS salon_name_gin_idx'
        ),
        migrations.RunSQL(
            'CREATE INDEX CONCURRENTLY "salon_city_gin_idx" ON "salon" USING GIN(city gin_trgm_ops);',
            reverse_sql='DROP INDEX CONCURRENTLY IF EXISTS salon_city_gin_idx'
        ),
        migrations.RunSQL(
            'CREATE INDEX CONCURRENTLY "stylist_service_name_gin_idx" ON "stylist_service" USING GIN(name gin_trgm_ops);',
            reverse_sql='DROP INDEX CONCURRENTLY IF EXISTS stylist_service_name_gin_idx'
        )
    ]
