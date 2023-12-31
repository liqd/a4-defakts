# Generated by Django 2.2.10 on 2020-02-26 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("sites", "0002_alter_domain_unique"),
        ("a4_candy_organisations", "0009_member_member_number"),
    ]

    operations = [
        migrations.AddField(
            model_name="organisation",
            name="site",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="sites.Site",
            ),
        ),
    ]
