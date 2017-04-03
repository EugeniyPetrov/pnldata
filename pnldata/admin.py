from django.contrib import admin
from django.db.models import Sum

from .models import Currency
from .models import Purse
from .models import Transaction
from .models import Expense
from .models import Tag

class ExpenseInline(admin.StackedInline):
    model = Expense
    extra = 1

class TransactionAdmin(admin.ModelAdmin):
    inlines = [ExpenseInline]
    list_display=('date', 'description', 'tag1', 'tag2', 'tag3',)

class ExpenseAdmin(admin.ModelAdmin):
    list_display=('get_transaction_id', 'get_transaction_date', 'amount', 'currency', 'purse', 'purse_amount', 'get_transaction_description', 'get_transaction_tag1', 'get_transaction_tag2', 'get_transaction_tag3',)

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

class PurseAdmin(admin.ModelAdmin):
    list_display=('balance',)

    def get_queryset(self, request):
        qs = super(PurseAdmin, self).get_queryset(request)
        return qs.annotate(balance=Sum('expense__purse_amount'))

    def balance(self, obj):
        return obj.balance

    balance.admin_order_field = 'balance'


admin.site.register(Currency)
admin.site.register(Purse, PurseAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Tag)
