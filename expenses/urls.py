from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView
urlpatterns = [
    path('hello/',views.helllo),
    path('',views.expense_list,name='expense_list'),
    path('addExpense/',views.add_expense,name='add_expense'),

    # For editing
    path('edit/<int:pk>/',views.edit,name='edit'),

    # For dashboard
    path('dashboard/',views.dashboard,name="dashboard"),

    # For registration of user
    path('register/',views.register,name="register"),

    # For login and logout
    path('login/',views.email_login,name='login'),
    path("logout/",LogoutView.as_view(next_page="login"),name="logout"),
    
    # For delete
    path('delete/<int:pk>/',views.delete,name='delete'),

    # Export to csv
    path('export/',views.export_csv,name='export'),

    # Export Filtered CSV
    path('export_filtered',views.export_filtered_csv,name="filtered_csv")
]