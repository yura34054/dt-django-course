from django.contrib import admin

from app.internal.models.bank_card import BankCard


@admin.register(BankCard)
class BankCardAdmin(admin.ModelAdmin):
    pass
