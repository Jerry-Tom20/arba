# Generated by Django 4.1.1 on 2023-05-08 10:43

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('arba_app', '0006_categories_cat_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='pro_slug',
            field=autoslug.fields.AutoSlugField(default=None, editable=False, null=True, populate_from='title', unique=True),
        ),
    ]