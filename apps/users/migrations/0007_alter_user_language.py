# Generated by Django 3.2.19 on 2023-10-17 09:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("a4_candy_users", "0006_change_error_wording_email_address"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="language",
            field=models.CharField(
                choices=[("en", "English"), ("de", "German")],
                default="de",
                help_text="Specify your preferred language for the user interface and the notifications of the platform.",
                max_length=4,
                verbose_name="Your preferred language",
            ),
        ),
    ]