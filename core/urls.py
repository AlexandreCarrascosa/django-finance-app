from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name = 'index'),
  path('login/', views.login_user, name="login"),
  path('login/submit', views.submit_login, name="submit"),
  path('register/', views.register_user, name="register"),
  path('logout/', views.logout_user, name="logout"),
  path('input/', views.insertInput, name='insertInput'),
  path('output/', views.insertOutput, name='insertOutput'),
  path('accounts/', views.accounts, name='accounts'),
  path('accounts/delete/<account>', views.delete_account, name='delete_account'),
  path('accounts/new/', views.create_account, name='new_account'),
  path('accounts/edit/<account>', views.edit_account, name="edit_account"),
  path('extract/', views.extract, name="extract"),
]

