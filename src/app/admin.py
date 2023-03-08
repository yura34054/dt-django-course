from django.contrib import admin

from app.internal.admin.admin_user import AdminUserAdmin
from app.internal.admin.user import UserAdmin
from app.internal.admin.bank_account import BankAccountAdmin

admin.site.site_title = "Backend course"
admin.site.site_header = "Backend course"
