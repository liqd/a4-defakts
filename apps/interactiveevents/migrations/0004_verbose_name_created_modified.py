# Generated by Django 3.2.18 on 2023-03-07 13:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        (
            "a4_candy_interactive_events",
            "0003_extrafieldsinteractiveevent_add_event_image",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="livequestion",
            name="created",
            field=models.DateTimeField(
                default=django.utils.timezone.now,
                editable=False,
                verbose_name="Created",
            ),
        ),
        migrations.AlterField(
            model_name="livequestion",
            name="modified",
            field=models.DateTimeField(
                blank=True, editable=False, null=True, verbose_name="Modified"
            ),
        ),
    ]
