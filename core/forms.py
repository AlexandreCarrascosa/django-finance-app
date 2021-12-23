from django import forms
from django.db.models import fields
from django.forms import ModelForm, DateInput, DecimalField, BooleanField, widgets
from django.utils.translation import gettext_lazy as _
from .models import moneyInputer, moneyOutputs, totalBalance

class addInput(ModelForm):
    
    repeat_input = BooleanField(label='Repetir operação neste dia',
                                required=False)
    
    class Meta:
        model = moneyInputer
        fields = ['title',
                  'value',
                  'input_date',
                  'account',
                  ]
    
        
        widgets = {
            'input_date': DateInput(format=('%d/%m/%Y'),
                                    attrs={'class': 'form-control',
                                           'type': 'date'}),

        }
        
    def __init__(self, user=None, **kwargs):
        super(addInput, self).__init__(**kwargs)
        if user:
            self.fields['account'].queryset= totalBalance.objects.filter(user=user)
        

class addOutput(ModelForm):
    class Meta:
        model = moneyOutputs
        fields = ['title',
                  'description',
                  'value',
                  'output_date',
                  'payment_type',
                  'installments',
                  'account']
        labels = {'description': 'Descrição',
                  'payment_type': 'Forma de Pagamento'}
        widgets = {
            'output_date': DateInput(format=('%d/%m/%Y'),
                                     attrs = {'class': 'form-control',
                                              'placeholder': 'Dia da compra',
                                              'type': 'date'}),
        }
        
    def __init__(self, user=None, **kwargs):
        super(addOutput, self).__init__(**kwargs)
        if user:
            self.fields['account'].queryset= totalBalance.objects.filter(user=user)
        
        
        

class addAccount(ModelForm):
    
    class Meta:
        model = totalBalance
        fields = ['account',
                  'bank',
                  'balance']
        
        labels = {'account': 'Conta',
                  'bank': 'Banco',
                  'balance': 'Saldo'}
        
        error_messages = {
            'account': {
                'unique': _("Eii.. essa conta já está registrada!"),
            },
            'balance': {
                'max_digits': _("Ops!! Esse saldo é um pouco grande, insira um valor de até 20 digitos!"),
            } ,        
        }
    
    
        
        
