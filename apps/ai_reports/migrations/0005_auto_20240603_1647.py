# Generated by Django 3.2.19 on 2024-06-03 14:47

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("ai_reports", "0004_migrate_fields_to_json"),
    ]

    operations = [
        migrations.RenameField(
            model_name="aireport",
            old_name="confidence_json",
            new_name="confidence",
        ),
        migrations.RenameField(
            model_name="aireport",
            old_name="explanation_json",
            new_name="explanation",
        ),
    ]
