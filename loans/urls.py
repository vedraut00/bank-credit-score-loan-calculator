from django.urls import path
from . import views

app_name = 'loans'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Customer views
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/create/', views.customer_create, name='customer_create'),
    path('customers/<int:customer_id>/', views.customer_detail, name='customer_detail'),
    path('customers/<int:customer_id>/edit/', views.customer_edit, name='customer_edit'),
    path('customers/<int:customer_id>/delete/', views.customer_delete, name='customer_delete'),
    
    # Loan views
    path('loans/', views.loan_list, name='loan_list'),
    path('loans/create/', views.loan_create, name='loan_create'),
    path('loans/<int:loan_id>/', views.loan_detail, name='loan_detail'),
    path('loans/<int:loan_id>/edit/', views.loan_edit, name='loan_edit'),
    path('loans/<int:loan_id>/delete/', views.loan_delete, name='loan_delete'),
    
    # Excel upload
    path('excel-upload/', views.excel_upload, name='excel_upload'),
    
    # Data management
    path('delete-all/', views.delete_all_data, name='delete_all_data'),
    
    # API endpoints
    path('api/customers/', views.api_customers, name='api_customers'),
    path('api/loans/', views.api_loans, name='api_loans'),
    path('api/credit-score/<int:customer_id>/', views.api_credit_score, name='api_credit_score'),
    path('api/loan-approval/<int:loan_id>/', views.api_loan_approval, name='api_loan_approval'),
]