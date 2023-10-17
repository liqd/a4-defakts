# Generated by Django 3.2.19 on 2023-10-17 09:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("a4_candy_organisations", "0021_alter_organisation_logo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="organisation",
            name="language",
            field=models.CharField(
                choices=[("en", "English"), ("de", "German")],
                default="de",
                help_text="All e-mails to unregistered users (invites) will be sent in this language.",
                max_length=4,
                verbose_name="Default language for e-mails",
            ),
        ),
    ]
