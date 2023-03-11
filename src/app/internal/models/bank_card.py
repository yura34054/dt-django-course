from django.db import models

from app.internal.models.bank_account import BankAccount


class BankCard(models.Model):
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Bank card"
        verbose_name_plural = "Bank cards"
