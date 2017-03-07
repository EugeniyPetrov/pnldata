from django.contrib import admin

from .models import Currency
from .models import Purse
from .models import ExpenseSet
from .models import Expense
from .models import Tag

class ExpenseInline(admin.StackedInline):
    model = Expense
    extra = 1

class ExpenseSetAdmin(admin.ModelAdmin):
    inlines = [ExpenseInline]
    list_display=('date', 'description', 'tag1', 'tag2', 'tag3',)

class ExpenseAdmin(admin.ModelAdmin):
    list_display=('get_expense_set_id', 'get_expense_set_date', 'amount', 'currency', 'purse', 'purse_amount', 'get_expense_set_description', 'get_expense_set_tag1', 'get_expense_set_tag2', 'get_expense_set_tag3',)

    def get_expense_set_id(self, obj):
        return obj.expense_set.id

    def get_expense_set_date(self, obj):
        return obj.expense_set.date

    def get_expense_set_description(self, obj):
        return obj.expense_set.description

    def get_expense_set_tag1(self, obj):
        return obj.expense_set.tag1

    def get_expense_set_tag2(self, obj):
        return obj.expense_set.tag2

    def get_expense_set_tag3(self, obj):
        return obj.expense_set.tag3

admin.site.register(Currency)
admin.site.register(Purse)
admin.site.register(ExpenseSet, ExpenseSetAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Tag)
