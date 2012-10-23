from django.contrib import admin
from .models import Balance, BalanceRow
from .models import Bill, Drink, Expense, Dinner

class RowInline(admin.TabularInline):
    model = BalanceRow
    extra = 1

class BalanceAdmin(admin.ModelAdmin):
    inlines = [
        RowInline,
    ]

admin.site.register(Balance, BalanceAdmin)
admin.site.register(Bill)
admin.site.register(BalanceRow)
admin.site.register(Drink)
admin.site.register(Expense)
admin.site.register(Dinner)

