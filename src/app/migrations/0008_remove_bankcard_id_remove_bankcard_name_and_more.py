# Generated by Django 4.2 on 2023-04-13 08:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0007_user_friends"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="bankcard",
            name="id",
        ),
        migrations.RemoveField(
            model_name="bankcard",
            name="name",
        ),
        migrations.AddField(
            model_name="bankcard",
            name="card_id",
            field=models.AutoField(default=None, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="user",
            name="friends",
            field=models.ManyToManyField(blank=True, null=True, to="app.user"),
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("time", models.DateTimeField(auto_now_add=True)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=11)),
                (
                    "account_from",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="account_from", to="app.bankaccount"
                    ),
                ),
                (
                    "account_to",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="account_to", to="app.bankaccount"
                    ),
                ),
                (
                    "card_from",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="card_from",
                        to="app.bankcard",
                    ),
                ),
                (
                    "card_to",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="card_to",
                        to="app.bankcard",
                    ),
                ),
            ],
            options={
                "verbose_name": "Transaction",
                "verbose_name_plural": "Transactions",
                "ordering": ["time"],
            },
        ),
    ]
