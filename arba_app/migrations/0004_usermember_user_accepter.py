# Generated by Django 4.1.1 on 2023-05-03 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arba_app', '0003_rename_image_products_pro_image_products_cat'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermember',
            name='user_accepter',
            field=models.BooleanField(null=True),
        ),
    ]