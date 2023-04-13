from django.db import models

from app.internal.models.bank_account import BankAccount


class BankCard(models.Model):
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.bank_account.owner.telegram_id}: {self.name}"

    class Meta:
        verbose_name = "Bank card"
        verbose_name_plural = "Bank cards"
