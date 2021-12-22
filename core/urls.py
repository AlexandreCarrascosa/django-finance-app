from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name = 'index'),
  path('input/', views.insertInput, name='insertInput'),
  path('output/', views.insertOutput, name='insertOutput'),
  path('accounts/', views.accounts, name='accounts'),
  path('accounts/new', views.create_account, name='new_account')

]

