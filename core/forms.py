from django import forms
from django.db.models import fields
from django.forms import ModelForm, DateInput, DecimalField, BooleanField
from .models import moneyInputer, moneyOutputs

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