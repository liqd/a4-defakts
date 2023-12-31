# Generated by Django 2.2.6 on 2019-10-24 12:19

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("wagtailcore", "0041_group_collection_permissions_verbose_name_plural"),
        ("a4_candy_cms_images", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="FormPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.Page",
                    ),
                ),
                (
                    "to_address",
                    models.CharField(
                        blank=True,
                        help_text="Optional - form submissions will be emailed to these addresses. Separate multiple addresses by comma.",
                        max_length=255,
                        verbose_name="to address",
                    ),
                ),
                (
                    "from_address",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="from address"
                    ),
                ),
                (
                    "subject",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="subject"
                    ),
                ),
                (
                    "header_de",
                    models.CharField(blank=True, max_length=500, verbose_name="Header"),
                ),
                (
                    "header_en",
                    models.CharField(blank=True, max_length=500, verbose_name="Header"),
                ),
                ("intro_en", wagtail.fields.RichTextField(blank=True)),
                ("intro_de", wagtail.fields.RichTextField(blank=True)),
                ("thank_you_text_en", models.TextField(blank=True)),
                ("thank_you_text_de", models.TextField(blank=True)),
                ("contact_person_name", models.CharField(blank=True, max_length=100)),
                (
                    "contact_person_image",
                    models.ForeignKey(
                        blank=True,
                        help_text="The Image will be shown besides the name of the contact person",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="a4_candy_cms_images.CustomImage",
                        verbose_name="Image of contact person",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page",),
        ),
        migrations.CreateModel(
            name="FormField",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "sort_order",
                    models.IntegerField(blank=True, editable=False, null=True),
                ),
                (
                    "label",
                    models.CharField(
                        help_text="The label of the form field",
                        max_length=255,
                        verbose_name="label",
                    ),
                ),
                (
                    "field_type",
                    models.CharField(
                        choices=[
                            ("singleline", "Single line text"),
                            ("multiline", "Multi-line text"),
                            ("email", "Email"),
                            ("number", "Number"),
                            ("url", "URL"),
                            ("checkbox", "Checkbox"),
                            ("checkboxes", "Checkboxes"),
                            ("dropdown", "Drop down"),
                            ("multiselect", "Multiple select"),
                            ("radio", "Radio buttons"),
                            ("date", "Date"),
                            ("datetime", "Date/time"),
                            ("hidden", "Hidden field"),
                        ],
                        max_length=16,
                        verbose_name="field type",
                    ),
                ),
                (
                    "required",
                    models.BooleanField(default=True, verbose_name="required"),
                ),
                (
                    "choices",
                    models.TextField(
                        blank=True,
                        help_text="Comma separated list of choices. Only applicable in checkboxes, radio and dropdown.",
                        verbose_name="choices",
                    ),
                ),
                (
                    "default_value",
                    models.CharField(
                        blank=True,
                        help_text="Default value. Comma separated values supported for checkboxes.",
                        max_length=255,
                        verbose_name="default value",
                    ),
                ),
                (
                    "help_text",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="help text"
                    ),
                ),
                (
                    "page",
                    modelcluster.fields.ParentalKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="form_fields",
                        to="a4_candy_cms_contacts.FormPage",
                    ),
                ),
            ],
            options={
                "ordering": ["sort_order"],
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="CustomFormSubmission",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("form_data", models.TextField()),
                (
                    "submit_time",
                    models.DateTimeField(auto_now_add=True, verbose_name="submit time"),
                ),
                ("email", models.EmailField(max_length=254)),
                ("message", models.TextField()),
                ("telephone_number", models.CharField(blank=True, max_length=100)),
                ("name", models.CharField(blank=True, max_length=100)),
                (
                    "page",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="wagtailcore.Page",
                    ),
                ),
            ],
            options={
                "verbose_name": "form submission",
                "abstract": False,
            },
        ),
    ]
