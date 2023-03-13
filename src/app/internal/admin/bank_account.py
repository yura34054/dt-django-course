from django.contrib import admin

from app.internal.models.bank_account import BankAccount


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    pass
