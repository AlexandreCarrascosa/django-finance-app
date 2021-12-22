from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class totalBalance(models.Model):
  '''
  This class contain all infos about
  accounts of users.
  
  Parameters:
             account (text): get account number, this is the primary key
             bank (text): get the name of bank that account is registered
             balance (numeric): get the current value in account at registration time
             register_date (datafield): autofield that get data that account is registered in system  
  '''
  account = models.CharField(max_length=8,
                             verbose_name="Conta",
                             primary_key=True)
  
  bank = models.CharField(max_length=100, 
                          verbose_name="Banco", 
                          )
  
  balance = models.DecimalField(max_digits=20,
                                decimal_places=2, 
                                verbose_name="Saldo",
                                
                                )
  
  register_date = models.DateTimeField(auto_now=True, 
                                       verbose_name="Inserido em")
  
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  
  class Meta:
    db_table = 'totalBalance'
    
  def __str__(self):
    return self.bank


class moneyInputer(models.Model):
  '''
  This model recive all infos about
  inputs values, like salary, tickets,
  etc..
  '''
  
  title = models.CharField(max_length=100,
                           verbose_name="Origem",
                           )
  
  value = models.DecimalField(max_digits=20,
                              decimal_places=2,
                              verbose_name="Valor")
  
  input_date = models.DateField(verbose_name="Data de pagamento")
  
  account = models.ForeignKey('totalBalance', 
                              on_delete=models.CASCADE,
                              verbose_name="Conta"
                              )
  
  
  def __str__(self):
    return self.title

class moneyOutputs(models.Model):
  title = models.CharField(max_length=100,
                           verbose_name="Título",
                           )
  
  description = models.TextField(blank=True,
                                 null=True)
  
  value = models.DecimalField(max_digits=20,
                              decimal_places=2,
                              verbose_name="Valor")
  
  output_date = models.DateField(verbose_name="Data de compra")
  
  PAYMENTS_LIST = (
    ('CV', 'Crédito à vista'),
    ('CP', 'Crédito parcelado'),
    ('D', 'Débito')
  )
  
  payment_type = models.CharField(max_length=10,
                                  choices=PAYMENTS_LIST,
                                  ) 
  
  installments = models.DecimalField(max_digits=2,
                                     decimal_places=0,
                                     default=0,
                                     verbose_name="Parcelas")
  
  account = models.ForeignKey('totalBalance',
                              on_delete=models.CASCADE,
                              verbose_name="Conta")
  



  def __str__(self):
    return self.title
  
  def get_output_values(self):
    return self.value * -1



