from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('expense/', views.expense_tracking, name='expense'),
    path('financial-dashboard/', views.financial_dashboard, name='financial_dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('budget-goals/', views.budget_goals, name='budget_goals'),
    path('create-budget/', views.create_budget, name='create_budget'),
    path('create-goal/', views.create_goal, name='create_goal'),

]