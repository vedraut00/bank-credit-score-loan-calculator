from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Count, Sum, Avg, Q
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, timedelta
import json
import pandas as pd
import io

from .models import Customer, Loan
from .serializers import CustomerSerializer, LoanDetailSerializer
from .utils import calculate_credit_score, determine_loan_approval


def dashboard(request):
    """Main dashboard view with system statistics"""
    try:
        # Get basic statistics
        total_customers = Customer.objects.count()
        total_loans = Loan.objects.count()
        total_loan_amount = Loan.objects.aggregate(total=Sum('loan_amount'))['total'] or 0
        
        # Recent activities
        recent_customers = Customer.objects.order_by('-created_at')[:5]
        recent_loans = Loan.objects.order_by('-created_at')[:5]
        
        # Credit score distribution
        customers_with_scores = []
        for customer in Customer.objects.all():
            score = calculate_credit_score(customer)
            customers_with_scores.append(score)
        
        score_distribution = {
            'excellent': len([s for s in customers_with_scores if s >= 800]),
            'good': len([s for s in customers_with_scores if 700 <= s < 800]),
            'fair': len([s for s in customers_with_scores if 600 <= s < 700]),
            'poor': len([s for s in customers_with_scores if s < 600])
        }
        
        context = {
            'total_customers': total_customers,
            'total_loans': total_loans,
            'total_loan_amount': total_loan_amount,
            'recent_customers': recent_customers,
            'recent_loans': recent_loans,
            'score_distribution': score_distribution,
        }
        return render(request, 'loans/dashboard.html', context)
    except Exception as e:
        # Fallback to simple dashboard if database is not available
        context = {
            'total_customers': 0,
            'total_loans': 0,
            'total_loan_amount': 0,
            'recent_customers': [],
            'recent_loans': [],
            'score_distribution': {
                'excellent': 0,
                'good': 0,
                'fair': 0,
                'poor': 0
            },
            'error_message': f"Database not available: {str(e)}"
        }
        return render(request, 'loans/dashboard.html', context)


def customer_list(request):
    """List all customers with search and pagination"""
    customers = Customer.objects.all().order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        customers = customers.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(phone_number__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(customers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'loans/customer_list.html', context)


def customer_detail(request, customer_id):
    """View customer details and their loans"""
    customer = get_object_or_404(Customer, customer_id=customer_id)
    loans = customer.loans.all().order_by('-created_at')
    credit_score = calculate_credit_score(customer)
    
    context = {
        'customer': customer,
        'loans': loans,
        'credit_score': credit_score,
    }
    return render(request, 'loans/customer_detail.html', context)


def customer_create(request):
    """Create new customer"""
    if request.method == 'POST':
        try:
            customer = Customer(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                age=int(request.POST['age']),
                phone_number=request.POST['phone_number'],
                monthly_salary=float(request.POST['monthly_salary']),
                approved_limit=float(request.POST['approved_limit']),
                current_debt=float(request.POST.get('current_debt', 0))
            )
            customer.full_clean()
            customer.save()
            messages.success(request, 'Customer created successfully!')
            return redirect('customer_detail', customer_id=customer.customer_id)
        except Exception as e:
            messages.error(request, f'Error creating customer: {str(e)}')
    
    return render(request, 'loans/customer_form.html', {'action': 'Create'})


def customer_edit(request, customer_id):
    """Edit existing customer"""
    customer = get_object_or_404(Customer, customer_id=customer_id)
    
    if request.method == 'POST':
        try:
            customer.first_name = request.POST['first_name']
            customer.last_name = request.POST['last_name']
            customer.age = int(request.POST['age'])
            customer.phone_number = request.POST['phone_number']
            customer.monthly_salary = float(request.POST['monthly_salary'])
            customer.approved_limit = float(request.POST['approved_limit'])
            customer.current_debt = float(request.POST.get('current_debt', 0))
            customer.full_clean()
            customer.save()
            messages.success(request, 'Customer updated successfully!')
            return redirect('customer_detail', customer_id=customer.customer_id)
        except Exception as e:
            messages.error(request, f'Error updating customer: {str(e)}')
    
    context = {
        'customer': customer,
        'action': 'Edit'
    }
    return render(request, 'loans/customer_form.html', context)


def loan_list(request):
    """List all loans with search and pagination"""
    loans = Loan.objects.select_related('customer').all().order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        loans = loans.filter(
            Q(customer__first_name__icontains=search_query) |
            Q(customer__last_name__icontains=search_query) |
            Q(loan_id__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(loans, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'loans/loan_list.html', context)


def loan_detail(request, loan_id):
    """View loan details and approval status"""
    loan = get_object_or_404(Loan, loan_id=loan_id)
    customer = loan.customer
    credit_score = calculate_credit_score(customer)
    approval_status = determine_loan_approval(customer, loan)
    
    context = {
        'loan': loan,
        'customer': customer,
        'credit_score': credit_score,
        'approval_status': approval_status,
    }
    return render(request, 'loans/loan_detail.html', context)


def loan_create(request):
    """Create new loan"""
    customers = Customer.objects.all()
    
    if request.method == 'POST':
        try:
            customer = get_object_or_404(Customer, customer_id=request.POST['customer_id'])
            loan = Loan(
                customer=customer,
                loan_amount=float(request.POST['loan_amount']),
                tenure=int(request.POST['tenure']),
                interest_rate=float(request.POST['interest_rate']),
                monthly_repayment=float(request.POST['monthly_repayment']),
                emis_paid_on_time=int(request.POST.get('emis_paid_on_time', 0)),
                start_date=request.POST['start_date'],
                end_date=request.POST['end_date']
            )
            loan.full_clean()
            loan.save()
            messages.success(request, 'Loan created successfully!')
            return redirect('loan_detail', loan_id=loan.loan_id)
        except Exception as e:
            messages.error(request, f'Error creating loan: {str(e)}')
    
    context = {
        'customers': customers,
        'action': 'Create'
    }
    return render(request, 'loans/loan_form.html', context)


def loan_edit(request, loan_id):
    """Edit existing loan"""
    loan = get_object_or_404(Loan, loan_id=loan_id)
    customers = Customer.objects.all()
    
    if request.method == 'POST':
        try:
            customer = get_object_or_404(Customer, customer_id=request.POST['customer_id'])
            loan.customer = customer
            loan.loan_amount = float(request.POST['loan_amount'])
            loan.tenure = int(request.POST['tenure'])
            loan.interest_rate = float(request.POST['interest_rate'])
            loan.monthly_repayment = float(request.POST['monthly_repayment'])
            loan.emis_paid_on_time = int(request.POST.get('emis_paid_on_time', 0))
            loan.start_date = request.POST['start_date']
            loan.end_date = request.POST['end_date']
            loan.full_clean()
            loan.save()
            messages.success(request, 'Loan updated successfully!')
            return redirect('loan_detail', loan_id=loan.loan_id)
        except Exception as e:
            messages.error(request, f'Error updating loan: {str(e)}')
    
    context = {
        'loan': loan,
        'customers': customers,
        'action': 'Edit'
    }
    return render(request, 'loans/loan_form.html', context)


def excel_upload(request):
    """Handle Excel file uploads for bulk data import"""
    if request.method == 'POST':
        try:
            excel_file = request.FILES.get('excel_file')
            if not excel_file:
                messages.error(request, 'Please select an Excel file.')
                return redirect('excel_upload')
            
            # Read Excel file
            df = pd.read_excel(excel_file)
            
            # Print debug information
            print(f"Excel file columns: {list(df.columns)}")
            print(f"Excel file shape: {df.shape}")
            print(f"First few rows: {df.head()}")
            
            # Determine file type based on columns
            if 'First Name' in df.columns:
                # Customer data
                success_count = 0
                error_count = 0
                for index, row in df.iterrows():
                    try:
                        # Handle missing values with actual column names
                        first_name = str(row.get('First Name', '')).strip()
                        last_name = str(row.get('Last Name', '')).strip()
                        age = int(row.get('Age', 25))
                        phone_number = str(row.get('Phone Number', '')).strip()
                        monthly_salary = float(row.get('Monthly Salary', 0))
                        approved_limit = float(row.get('Approved Limit', 0))
                        current_debt = float(row.get('Current Debt', 0))  # This column might not exist
                        
                        # Validate required fields
                        if not first_name or not last_name or not phone_number:
                            print(f"Row {index + 1}: Missing required fields")
                            error_count += 1
                            continue
                        
                        # Check if customer already exists
                        if Customer.objects.filter(phone_number=phone_number).exists():
                            print(f"Row {index + 1}: Customer with phone {phone_number} already exists")
                            error_count += 1
                            continue
                        
                        customer = Customer(
                            first_name=first_name,
                            last_name=last_name,
                            age=age,
                            phone_number=phone_number,
                            monthly_salary=monthly_salary,
                            approved_limit=approved_limit,
                            current_debt=current_debt
                        )
                        customer.full_clean()
                        customer.save()
                        success_count += 1
                        print(f"Row {index + 1}: Customer {first_name} {last_name} created successfully")
                        
                    except Exception as e:
                        print(f"Row {index + 1}: Error - {str(e)}")
                        error_count += 1
                        continue
                
                if success_count > 0:
                    messages.success(request, f'Successfully imported {success_count} customers from Excel file.')
                if error_count > 0:
                    messages.warning(request, f'{error_count} rows had errors and were skipped.')
            
            elif 'Loan Amount' in df.columns and 'Customer ID' in df.columns:
                # Loan data
                success_count = 0
                error_count = 0
                for index, row in df.iterrows():
                    try:
                        customer_id = int(row.get('Customer ID'))
                        loan_amount = float(row.get('Loan Amount', 0))
                        tenure = int(row.get('Tenure', 12))
                        interest_rate = float(row.get('Interest Rate', 10.0))
                        monthly_repayment = float(row.get('Monthly payment', 0))
                        emis_paid_on_time = int(row.get('EMIs paid on Time', 0))
                        
                        # Handle date conversion with actual column names
                        start_date = row.get('Date of Approval')
                        end_date = row.get('End Date')
                        
                        if pd.isna(start_date) or pd.isna(end_date):
                            print(f"Row {index + 1}: Missing start_date or end_date")
                            error_count += 1
                            continue
                        
                        # Convert dates properly
                        if isinstance(start_date, str):
                            start_date = pd.to_datetime(start_date).date()
                        elif hasattr(start_date, 'date'):
                            start_date = start_date.date()
                        else:
                            start_date = pd.to_datetime(start_date).date()
                            
                        if isinstance(end_date, str):
                            end_date = pd.to_datetime(end_date).date()
                        elif hasattr(end_date, 'date'):
                            end_date = end_date.date()
                        else:
                            end_date = pd.to_datetime(end_date).date()
                        
                        # Validate customer exists
                        try:
                            customer = Customer.objects.get(customer_id=customer_id)
                        except Customer.DoesNotExist:
                            print(f"Row {index + 1}: Customer with ID {customer_id} does not exist")
                            error_count += 1
                            continue
                        
                        loan = Loan(
                            customer=customer,
                            loan_amount=loan_amount,
                            tenure=tenure,
                            interest_rate=interest_rate,
                            monthly_repayment=monthly_repayment,
                            emis_paid_on_time=emis_paid_on_time,
                            start_date=start_date,
                            end_date=end_date
                        )
                        loan.full_clean()
                        loan.save()
                        success_count += 1
                        print(f"Row {index + 1}: Loan for customer {customer_id} created successfully")
                        
                    except Exception as e:
                        print(f"Row {index + 1}: Error - {str(e)}")
                        error_count += 1
                        continue
                
                if success_count > 0:
                    messages.success(request, f'Successfully imported {success_count} loans from Excel file.')
                if error_count > 0:
                    messages.warning(request, f'{error_count} rows had errors and were skipped.')
            
            else:
                messages.error(request, f'Unrecognized Excel file format. Found columns: {list(df.columns)}. Please check the column headers.')
            
        except Exception as e:
            print(f"Excel processing error: {str(e)}")
            messages.error(request, f'Error processing Excel file: {str(e)}')
    
    return render(request, 'loans/excel_upload.html')


def customer_delete(request, customer_id):
    """Delete a customer and all their loans"""
    customer = get_object_or_404(Customer, customer_id=customer_id)
    
    if request.method == 'POST':
        try:
            customer_name = f"{customer.first_name} {customer.last_name}"
            # Delete customer (this will cascade delete all loans due to ForeignKey)
            customer.delete()
            messages.success(request, f'Customer "{customer_name}" and all their loans have been deleted successfully.')
            return redirect('loans:customer_list')
        except Exception as e:
            messages.error(request, f'Error deleting customer: {str(e)}')
    
    context = {
        'customer': customer,
        'loan_count': customer.loans.count()
    }
    return render(request, 'loans/customer_delete_confirm.html', context)


def loan_delete(request, loan_id):
    """Delete a specific loan"""
    loan = get_object_or_404(Loan, loan_id=loan_id)
    
    if request.method == 'POST':
        try:
            loan_info = f"Loan {loan.loan_id} (${loan.loan_amount})"
            loan.delete()
            messages.success(request, f'Loan "{loan_info}" has been deleted successfully.')
            return redirect('loans:loan_list')
        except Exception as e:
            messages.error(request, f'Error deleting loan: {str(e)}')
    
    context = {
        'loan': loan
    }
    return render(request, 'loans/loan_delete_confirm.html', context)


def delete_all_data(request):
    """Delete all customers and loans from the system"""
    if request.method == 'POST':
        try:
            # Get counts before deletion
            customer_count = Customer.objects.count()
            loan_count = Loan.objects.count()
            
            # Delete all data
            Customer.objects.all().delete()  # This will cascade delete all loans
            
            messages.success(request, f'All data has been deleted successfully! ({customer_count} customers and {loan_count} loans removed)')
            return redirect('loans:dashboard')
        except Exception as e:
            messages.error(request, f'Error deleting all data: {str(e)}')
    
    # Get current data counts
    context = {
        'customer_count': Customer.objects.count(),
        'loan_count': Loan.objects.count(),
        'total_loan_amount': Loan.objects.aggregate(total=Sum('loan_amount'))['total'] or 0
    }
    return render(request, 'loans/delete_all_confirm.html', context)


def api_customers(request):
    """API endpoint for customer data"""
    customers = Customer.objects.all()
    serializer = CustomerSerializer(customers, many=True)
    return JsonResponse(serializer.data, safe=False)


def api_loans(request):
    """API endpoint for loan data"""
    loans = Loan.objects.select_related('customer').all()
    serializer = LoanDetailSerializer(loans, many=True)
    return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def api_credit_score(request, customer_id):
    """API endpoint to calculate credit score for a customer"""
    if request.method == 'POST':
        try:
            customer = get_object_or_404(Customer, customer_id=customer_id)
            credit_score = calculate_credit_score(customer)
            return JsonResponse({'credit_score': credit_score})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def api_loan_approval(request, loan_id):
    """API endpoint to check loan approval status"""
    if request.method == 'POST':
        try:
            loan = get_object_or_404(Loan, loan_id=loan_id)
            approval_status = determine_loan_approval(loan.customer, loan)
            return JsonResponse(approval_status)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
