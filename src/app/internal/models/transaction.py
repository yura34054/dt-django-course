from django.db import models
from django_prometheus.models import ExportModelOperationsMixin

from app.internal.models.bank_account import BankAccount
from app.internal.models.bank_card import BankCard


class Transaction(ExportModelOperationsMixin("transaction"), models.Model):
    time = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=11, decimal_places=2)

    card_from = models.ForeignKey(BankCard, blank=True, null=True, on_delete=models.SET_NULL, related_name="card_from")
    account_from = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name="account_from")

    card_to = models.ForeignKey(BankCard, blank=True, null=True, on_delete=models.SET_NULL, related_name="card_to")
    account_to = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name="account_to")

    def __str__(self):
        return f"{self.time}: {self.account_from.name} {self.amount} to {self.account_to.name}"

    class Meta:
        ordering = ["time"]
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
