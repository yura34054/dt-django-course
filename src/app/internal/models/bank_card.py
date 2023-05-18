from django.db import models
from django_prometheus.models import ExportModelOperationsMixin

from app.internal.models.bank_account import BankAccount


class BankCard(ExportModelOperationsMixin("bank_card"), models.Model):
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    card_id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.bank_account.owner.telegram_id}: {self.card_id}"

    class Meta:
        verbose_name = "Bank card"
        verbose_name_plural = "Bank cards"
