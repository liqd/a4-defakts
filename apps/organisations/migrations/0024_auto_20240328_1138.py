# Generated by Django 3.2.19 on 2024-03-28 10:38

from django.db import migrations
import django_ckeditor_5.fields


class Migration(migrations.Migration):
    dependencies = [
        ("a4_candy_organisations", "0023_alter_organisationtranslation_information"),
    ]

    operations = [
        migrations.AlterField(
            model_name="organisation",
            name="data_protection",
            field=django_ckeditor_5.fields.CKEditor5Field(
                blank=True,
                help_text="Please provide all the legally required information of your data protection. The data protection policy will be shown on a separate page.",
                verbose_name="Data protection policy",
            ),
        ),
        migrations.AlterField(
            model_name="organisation",
            name="imprint",
            field=django_ckeditor_5.fields.CKEditor5Field(
                blank=True,
                help_text="Please provide all the legally required information of your imprint. The imprint will be shown on a separate page.",
                verbose_name="Imprint",
            ),
        ),
        migrations.AlterField(
            model_name="organisation",
            name="netiquette",
            field=django_ckeditor_5.fields.CKEditor5Field(
                blank=True,
                help_text="Please provide a netiquette for the participants. The netiquette helps improving the climate of online discussions and supports the moderation.",
                verbose_name="Netiquette",
            ),
        ),
        migrations.AlterField(
            model_name="organisation",
            name="terms_of_use",
            field=django_ckeditor_5.fields.CKEditor5Field(
                blank=True,
                help_text="Please provide all the legally required information of your terms of use. The terms of use will be shown on a separate page.",
                verbose_name="Terms of use",
            ),
        ),
    ]