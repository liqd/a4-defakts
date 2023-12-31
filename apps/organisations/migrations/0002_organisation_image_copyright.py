# Generated by Django 2.2.6 on 2019-12-09 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("a4_candy_organisations", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="organisation",
            name="image_copyright",
            field=models.CharField(
                blank=True,
                help_text="Author, which is displayed in the header image.",
                max_length=200,
                verbose_name="Header image copyright",
            ),
        ),
    ]
