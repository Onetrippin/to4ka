from django.contrib import admin

from app.internal.presentation.admin.admin_user import AdminUserAdmin
from app.internal.presentation.admin.balance import BalanceAdmin
from app.internal.presentation.admin.order import OrderAdmin
from app.internal.presentation.admin.tool import ToolAdmin
from app.internal.presentation.admin.trade import TradeAdmin
from app.internal.presentation.admin.user import UserAdmin
from app.internal.presentation.admin.user_tool import UserToolAdmin

admin.site.site_title = 'To4ka administration'
admin.site.site_header = 'To4ka administration'
