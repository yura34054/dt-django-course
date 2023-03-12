from django.db import models


class BankAccount(models.Model):
    owner_id = models.IntegerField()
    account_id = models.IntegerField()
    money = models.DecimalField(max_digits=11, decimal_places=2)

    def __str__(self):
        return f"{self.owner_id}: {self.account_id}"

    class Meta:
        verbose_name = "Bank account"
        verbose_name_plural = "Bank accounts"
