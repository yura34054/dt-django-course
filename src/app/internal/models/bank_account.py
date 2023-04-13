from django.db import models

from app.internal.models.user import User


class BankAccount(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)
    money = models.DecimalField(max_digits=11, decimal_places=2)

    def __str__(self):
        return f"{self.owner.telegram_id}: {self.name}"

    class Meta:
        verbose_name = "Bank account"
        verbose_name_plural = "Bank accounts"
