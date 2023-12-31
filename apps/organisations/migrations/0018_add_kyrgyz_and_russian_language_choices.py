# Generated by Django 2.2.19 on 2021-03-04 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "a4_candy_organisations",
            "0017_remove_untranslated_slogan_information_description",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="organisation",
            name="language",
            field=models.CharField(
                choices=[
                    ("en", "English"),
                    ("de", "German"),
                    ("nl", "Dutch"),
                    ("ky", "Kyrgyz"),
                    ("ru", "Russian"),
                ],
                default="de",
                help_text="All e-mails to unregistered users (invites) will be sent in this language.",
                max_length=4,
                verbose_name="Default language for e-mails",
            ),
        ),
    ]
