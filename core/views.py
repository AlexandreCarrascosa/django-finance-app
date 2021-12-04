from decimal import Decimal
from django.db.models import Sum, fields
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from .forms import *


def query_db():
  # Get all avaliable balance
  current_balance = totalBalance.objects.aggregate(total = Sum('balance'))['total']
  current_balance = f'R${current_balance :.2f}' if current_balance != None else 'R$0.00'
  
  # Get General Outputs
  outputs = moneyOutputs.objects.all()
  inputs = moneyInputer.objects.all()
  
  extracts = {
    'outputs': outputs,
    'inputs': inputs,
  }
  
  extract = []
  
  for key in extracts.keys():
    for extractvalue in extracts[key]:
      if key == 'outputs':
        extract.append((float(extractvalue.get_output_values()),
                        str(extractvalue.output_date))
                       )
      else:
        extract.append((float(extractvalue.value), 
                        str(extractvalue.input_date))
                       )
            
  # Get outpurs in debit
  outputs_debit = moneyOutputs.objects.filter(payment_type__startswith="D").all()
  
  values_outputs_debit = outputs_debit.aggregate(total = Sum('value'))['total']
   
  values_outputs_debit = f'R${values_outputs_debit :.2f}' if values_outputs_debit != None else 'R$0.00'
  
  
  # Get outputs in credit
  outputs_credit = moneyOutputs.objects.filter(
    payment_type__startswith="C"
    ).all()
  
  values_outputs_credit = outputs_credit.aggregate(total = Sum('value'))['total']
  values_outputs_credit = f'R${values_outputs_credit :.2f}' if values_outputs_credit != None else 'R$0.00'

  # Get all importants variables
  infos = {
    'current_balance': current_balance,
    'values_outputs_credit': values_outputs_credit,
    'values_outputs_debit': values_outputs_debit,
    'extract': extract,
  }

  return infos

def index(request):
  
  infos = query_db()
  
  if request.method == "POST":
    return HttpResponseRedirect(request.POST.get('moviment_type'))
       
  return render(request, 'index.html', context=infos)

def accounts(request):
  
  registered_accounts = totalBalance.objects.all()
  
  context = {
    'accounts': registered_accounts,
  }    
  
  return render(request, 'accounts.html', context=context)

def insertInput(request):
  
  infos = query_db()
  
  form = addInput(request.POST or None)
  infos['form'] = form
    
  if request.POST:
    if form.is_valid():
      title = request.POST.get('title')
      value = request.POST.get('value')
      input_date = request.POST.get('input_date')
      account_number = request.POST.get('account')   
      
      account = totalBalance.objects.get(account=account_number)
      
      account.balance += Decimal(float(value))
      account.save()
      
      moneyInputer.objects.create(title = title,
                                  value=value,
                                  input_date= input_date,
                                  account = account)
    
    
    
  if request.method == "POST":
    return HttpResponseRedirect(request.POST.get('moviment_type'))
  
  return render(request, 'form_input.html', context = infos)

def insertOutput(request):
  
  infos = query_db()
  
  form = addOutput(request.POST or None)
  infos['form'] = form
  
  if request.POST:
    if form.is_valid():
      title = request.POST.get('title')
      description = request.POST.get('description')
      value = request.POST.get('value')
      output_date = request.POST.get('output_date')
      payment_type = request.POST.get('payment_type')
      installments = request.POST.get('installments')
      
      account_number = request.POST.get('account')
      account = totalBalance.objects.get(account=account_number)
      
      if payment_type == "D":
        account.balance -= Decimal(float(value))
        account.save()
      
      moneyOutputs.objects.create(title=title,
                                  description = description,
                                  value = value,
                                  output_date = output_date,
                                  payment_type = payment_type,
                                  installments = installments,
                                  account = account)
      
  if request.method == "POST":
    return HttpResponseRedirect(request.POST.get('moviment_type'))
  
  
  return render(request, 'form_output.html', context=infos)


