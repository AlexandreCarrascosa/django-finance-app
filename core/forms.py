from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, DateInput, BooleanField, EmailField, widgets
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
                  'categories',
                  'description',
                  'value',
                  'output_date',
                  'payment_type',
                  'installments',
                  'account',
                  ]
        
        labels = {'description': 'Descrição',
                  'payment_type': 'Forma de Pagamento',
                  'categories': 'Categoria'}
        
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
    
    

class NewUser(UserCreationForm):

    email = EmailField(required=True,
                       help_text= None)
    
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username", 
            "email", 
            "password1", 
            "password2",
                  ]
                
        labels = {
            "username": "Usuário",
            "password1": "Senha",
            "password2": "Confirme sua Senha",
            "gender": "Gênero",
        }
        
    def save(self, commit=True):
        user = super(NewUser, self).save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
        
        return user
    
    def __init__(self, *args, **kwargs):
        super(NewUser, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None