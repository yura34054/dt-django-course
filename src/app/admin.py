from django.contrib import admin

from app.internal.admin.admin_user import AdminUserAdmin
from app.internal.admin.bank_account import BankAccountAdmin
from app.internal.admin.bank_card import BankCardAdmin
from app.internal.admin.transaction import TransactionAdmin
from app.internal.admin.user import UserAdmin

admin.site.site_title = "Backend course"
admin.site.site_header = "Backend course"
