from django.core.validators import RegexValidator
from django.db import models


class User(models.Model):
    telegram_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True)
    username = models.CharField(blank=True)
    phone_number = models.CharField(
        max_length=30,
        blank=True,
        validators=[
            RegexValidator(
                regex=r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$", message="Invalid phone number"
            )
        ],
    )
    friends = models.ManyToManyField("self", symmetrical=False, blank=True)
    password = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.telegram_id})"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
