from django.contrib.auth.models import AbstractUser


class AdminUser(AbstractUser):
    class Meta:
        verbose_name = "Admin"
        verbose_name_plural = "Admins"
