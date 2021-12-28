from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, fields
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect, render, resolve_url
from .models import *
from .forms import *


def query_db(user):
    # Get all avaliable balance
    
    current_balance = totalBalance.objects.filter(user=user).aggregate(total=Sum('balance'))['total']
    
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
    outputs_debit = moneyOutputs.objects.filter(        payment_type__startswith="D").all()

    values_outputs_debit = outputs_debit.aggregate(total=Sum('value'))['total']

    values_outputs_debit = f'R${values_outputs_debit :.2f}' if values_outputs_debit != None else 'R$0.00'

    # Get outputs in credit
    outputs_credit = moneyOutputs.objects.filter(
        payment_type__startswith="C"
    ).all()

    values_outputs_credit = outputs_credit.aggregate(total=Sum('value'))[
        'total']
    values_outputs_credit = f'R${values_outputs_credit :.2f}' if values_outputs_credit != None else 'R$0.00'

    # Get all importants variables
    infos = {
        'current_balance': current_balance,
        'values_outputs_credit': values_outputs_credit,
        'values_outputs_debit': values_outputs_debit,
        'extract': extract,
    }

    return infos

def login_user(request):
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

def submit_login(request):
    
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, 
                            password=password)
        
        print(username, password)
        
        if user is not None:
            login(request, user)
            return redirect('/')
        
        else:
            messages.error(request, "Erro: Usuário e/ou Senha Incorreto!")
        
    return redirect('/')

def register_user(request):
    
    form = NewUser(request.POST or None)

    if request.POST:
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Usuário Criado com Sucesso!!!")
            return redirect("/")

        else:
            
            messages.error(request, "O Cadastro do Usuário falhou 😥")
            for field in form:
                for error in field.errors:
                    print(field, error)                   
                    messages.error(request, error)
                       
            return HttpResponseRedirect(reverse('register'))
          
    context = {
        "form": form
    }
    
    
    
    return render(request, 'register.html', context=context)



@login_required(login_url="/login/")
def index(request):

    user = request.user
    infos = query_db(user)

    if request.method == "POST":
        return HttpResponseRedirect(request.POST.get('moviment_type'))
    
    context = {
        'infos': infos,
        'user': request.user,
    }

    return render(request, 'index.html', context=context)

def insertInput(request):

    user = request.user
    infos = query_db(user)

    # form = addInput(request.POST or None, user=user)
    form = addInput(user=user)
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

            moneyInputer.objects.create(title=title,
                                        value=value,
                                        input_date=input_date,
                                        account=account,
                                        )

    if request.method == "POST":
        return HttpResponseRedirect(request.POST.get('moviment_type'))

    return render(request, 'form_input.html', context=infos)


def insertOutput(request):

    user = request.user
    infos = query_db(user)

    form = addOutput(user=user)
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
            account = totalBalance.objects.filter(user=user).get(account=account_number)

            if payment_type == "D":
                account.balance -= Decimal(float(value))
                account.save()

            moneyOutputs.objects.create(title=title,
                                        description=description,
                                        value=value,
                                        output_date=output_date,
                                        payment_type=payment_type,
                                        installments=installments,
                                        account=account,
                                        )

    if request.method == "POST":
        return HttpResponseRedirect(request.POST.get('moviment_type'))

    return render(request, 'form_output.html', context=infos)


@login_required(login_url="/login/")
def accounts(request):
    '''
    This view function is use to read all accounts
    registered on database
    '''
    user = request.user
    
    registered_accounts = totalBalance.objects.filter(user=user)
    data = request.GET.get('account')    
    
    if data:
        
        messages.warning(request, 'Você tem certeza que deseja deletar essa conta? (Essa ação é irreversível!)')
    
    context = {
        'accounts': registered_accounts,
        'data': data,
    }
    
    

    return render(request, 'accounts.html', context=context)

@login_required(login_url="/login/")
def delete_account(request, account):
    
    if request.POST:
        
        try:
            query = totalBalance.objects.get(account=account)
        except Exception:
            raise Http404()
        
        text_confirm = request.POST.get('text-delete-confirm')
        base = f'{query.bank}/{query.account}'
        
        if text_confirm == base:

            query.delete()

        return HttpResponseRedirect(reverse('accounts'))
    
    pass

@login_required(login_url="/login/")
def create_account(request):
    '''
    This view function is used to add a new account and
    to Edit accounts

    '''
    
    infos = query_db(request.user)

    form = addAccount(request.POST or None)
    infos['form'] = form

    if request.POST:
                
        if form.is_valid():
            data = request.POST
            account = data.get('account')
            bank = data.get('bank')
            balance = data.get('balance')
            user = request.user    
                
            totalBalance.objects.create(
                account=account,
                bank=bank,
                balance=balance,
                user=user
            )
            

            messages.success(request, 'Conta registrada com sucesso!')

            return HttpResponseRedirect(reverse('new_account'))
          
        else:
          
          for field in form:
            for error in field.errors:
              print(field, error)                   
              messages.error(request, error)
          
          return HttpResponseRedirect(reverse('new_account'))

    return render(request, 'create_account.html', context=infos)

@login_required(login_url="/login/")
def edit_account(request, account):
    
    user = request.user
    info = totalBalance.objects.get(account=account)
    
    if user != info.user:
        return redirect('/')
    
    if request.POST:
        
        data = request.POST
        bank = data.get('bank')
        balance = data.get('balance')
                
        info.bank = bank
        info.balance = balance
        info.save()
        
        messages.success(request, f'Informações da conta {account} atualizadas!')
    
    bank = info.bank
    balance = str(info.balance)
    balance = balance.replace(',', '.')
       
    context = {
        'account': account,
        'bank': bank,
        'balance': balance,
    }
        
    
    return render(request, 'edit_account.html', context)


