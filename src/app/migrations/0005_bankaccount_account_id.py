# Generated by Django 4.2b1 on 2023-03-12 09:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0004_bankcard"),
    ]

    operations = [
        migrations.AddField(
            model_name="bankaccount",
            name="account_id",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]