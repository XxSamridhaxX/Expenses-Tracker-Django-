from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView
urlpatterns = [
    path('hello/',views.helllo),
    path('',views.expense_list,name='expense_list'),
    path('addExpense/',views.add_expense,name='add_expense'),

    # For registration of user
    path('register/',views.register,name="register"),

    # For login and logout
    path('login/',views.email_login,name='login'),
    path("logout/",LogoutView.as_view(next_page="login"),name="logout"),
]