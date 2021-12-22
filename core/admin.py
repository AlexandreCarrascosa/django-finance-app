from django.contrib import admin
from core.models import totalBalance, moneyInputer, moneyOutputs

class dashboardBalance(admin.ModelAdmin):
  list_display = ('account', 'bank', 'money_format', 'register_date', 'user')

  def money_format(self, obj):
    balance = f'R$ {obj.balance}'
    return balance
  
  money_format.admin_order_field = "balance"
  money_format.short_description = "Saldo"


@admin.register(moneyInputer)
class moneyInputerAdmin(admin.ModelAdmin):
  list_display = ('title', 'account', 'money_format', 'input_date' )
  
  def money_format(self, obj):
    value = f'R$ {obj.value}'
    return value
  
  money_format.admin_order_field= "value"
  money_format.short_description = "Valor"

@admin.register(moneyOutputs)
class moneyOutputsAdmin(admin.ModelAdmin):
  list_display = ('account', 'title', 'money_format', 'output_date', 'payment_type', 'installments' )
  
  def money_format(self, obj):
    value = f'R$ {obj.value}'
    return value
  
  money_format.admin_order_field= "value"
  money_format.short_description = "Valor"


admin.site.register(totalBalance, dashboardBalance)


# Register your models here.
