from django.contrib import admin
from django.db.models import Sum
import bulk_admin

from .models import Currency
from .models import Purse
from .models import Transaction
from .models import Expense
from .models import Tag

class ExpenseInline(admin.StackedInline):
    model = Expense
    readonly_fields=('purse_amount_usd', 'purse_amount_eur',)
    extra = 1

class TransactionAdmin(bulk_admin.BulkModelAdmin):
    inlines = [ExpenseInline]
    list_display=('date', 'description', 'tag1', 'tag2', 'tag3',)
    ordering=('-date',)

class ExpenseAdmin(bulk_admin.BulkModelAdmin):
    list_display=('get_transaction_id', 'get_transaction_date', 'amount', 'currency', 'purse', 'purse_amount', 'purse_amount_usd', 'purse_amount_eur', 'get_transaction_description', 'get_transaction_tag1', 'get_transaction_tag2', 'get_transaction_tag3',)
    list_filter=('purse',)
    ordering=('-transaction__date',)
    readonly_fields=('purse_amount_usd', 'purse_amount_eur',)

    def get_transaction_id(self, obj):
        return obj.transaction.id

    def get_transaction_date(self, obj):
        return obj.transaction.date

    def get_transaction_description(self, obj):
        return obj.transaction.description

    def get_transaction_tag1(self, obj):
        return obj.transaction.tag1

    def get_transaction_tag2(self, obj):
        return obj.transaction.tag2

    def get_transaction_tag3(self, obj):
        return obj.transaction.tag3

class PurseAdmin(bulk_admin.BulkModelAdmin):
    list_display=('__unicode__', 'balance', 'balance_usd', 'balance_eur',)

    def get_queryset(self, request):
        qs = super(PurseAdmin, self).get_queryset(request)
        return qs.annotate(balance=Sum('expense__purse_amount'), balance_usd=Sum('expense__purse_amount_usd'), balance_eur=Sum('expense__purse_amount_eur'))

    def balance(self, obj):
        return obj.balance

    def balance_usd(self, obj):
        return obj.balance_usd

    def balance_eur(self, obj):
        return obj.balance_eur

    balance.admin_order_field = 'balance'


admin.site.register(Currency)
admin.site.register(Purse, PurseAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Tag)
