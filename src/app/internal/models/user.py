from django.core.validators import RegexValidator
from django.db import models


class User(models.Model):
    chat_id = models.IntegerField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True)
    username = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(
        max_length=30,
        blank=True,
        validators=[
            RegexValidator(
                regex=r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$", message="Invalid phone number"
            )
        ],
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.chat_id})"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
