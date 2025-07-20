from decimal import Decimal
from datetime import datetime, date
from .models import Loan, Customer
import math


def calculate_credit_score(customer):
    """Calculate credit score based on historical data (300-850 range)"""
    loans = Loan.objects.filter(customer=customer)  # type: ignore
    
    if not loans.exists():  # type: ignore
        return 650  # Default score for new customers
    
    # Component 1: Past loans paid on time (40% weightage)
    total_emis = sum(loan.tenure for loan in loans)
    paid_on_time = sum(loan.emis_paid_on_time for loan in loans)
    on_time_ratio = paid_on_time / total_emis if total_emis > 0 else 0
    
    # Component 2: Number of loans taken (20% weightage)
    num_loans = loans.count()  # type: ignore
    
    # Component 3: Loan activity in current year (20% weightage)
    current_year = datetime.now().year
    current_year_loans = loans.filter(start_date__year=current_year).count()  # type: ignore
    
    # Component 4: Loan approved volume (20% weightage)
    total_loan_amount = sum(loan.loan_amount for loan in loans)
    
    # Component 5: Current debt vs approved limit
    current_debt = sum(
        loan.loan_amount for loan in loans 
        if loan.end_date > date.today()
    )
    
    # Base score starts at 300
    base_score = 300
    
    # Calculate score components (max 550 points to reach 850)
    score = base_score
    
    # Payment history (up to 220 points)
    score += on_time_ratio * 220
    
    # Loan history (up to 110 points)
    score += min(num_loans * 20, 110)
    
    # Current activity (up to 110 points)
    score += min(current_year_loans * 30, 110)
    
    # Volume bonus (up to 110 points)
    score += min(float(total_loan_amount) / 1000000 * 50, 110)
    
    # Penalty for high debt utilization
    if customer.approved_limit > 0:
        debt_utilization = (current_debt / customer.approved_limit) * 100
        if debt_utilization > 80:
            score -= 100
        elif debt_utilization > 60:
            score -= 50
        elif debt_utilization > 40:
            score -= 25
    
    # Ensure score is within valid range
    return min(max(int(score), 300), 850)


def calculate_monthly_installment(loan_amount, tenure, interest_rate):
    """Calculate monthly installment using compound interest formula"""
    P = float(loan_amount)
    r = float(interest_rate) / (12 * 100)  # Monthly interest rate
    n = int(tenure)  # Number of months
    
    if r == 0:
        return P / n
    
    # EMI = P * r * (1 + r)^n / ((1 + r)^n - 1)
    emi = P * r * (1 + r) ** n / ((1 + r) ** n - 1)
    return round(emi, 2)


def get_corrected_interest_rate(credit_score, requested_rate):
    """Get corrected interest rate based on credit score"""
    if credit_score > 50:
        return requested_rate  # No correction needed
    elif 30 < credit_score <= 50:
        return max(requested_rate, 12.0)
    elif 10 < credit_score <= 30:
        return max(requested_rate, 16.0)
    else:
        return None  # Loan not approved


def check_loan_eligibility(customer, loan_amount, interest_rate, tenure):
    """Check if customer is eligible for loan"""
    # Calculate credit score
    credit_score = calculate_credit_score(customer)
    
    # Check current EMIs
    current_loans = Loan.objects.filter(customer=customer, end_date__gt=date.today())  # type: ignore
    current_emis = sum(loan.monthly_repayment for loan in current_loans)
    
    # Calculate new EMI
    new_emi = calculate_monthly_installment(loan_amount, tenure, interest_rate)
    total_emis = current_emis + Decimal(str(new_emi))
    
    # Check if total EMIs exceed 50% of monthly salary
    if total_emis > customer.monthly_salary * Decimal('0.5'):
        return False, credit_score, None
    
    # Check credit score eligibility
    if credit_score > 50:
        return True, credit_score, interest_rate
    elif 30 < credit_score <= 50 and interest_rate >= 12:
        return True, credit_score, max(interest_rate, 12.0)
    elif 10 < credit_score <= 30 and interest_rate >= 16:
        return True, credit_score, max(interest_rate, 16.0)
    else:
        return False, credit_score, None


def round_to_nearest_lakh(amount):
    """Round amount to nearest lakh"""
    return round(amount / 100000) * 100000


def determine_loan_approval(customer, loan):
    """Determine loan approval status based on customer and loan data"""
    # Calculate credit score
    credit_score = calculate_credit_score(customer)
    
    # Check if loan amount exceeds approved limit
    if loan.loan_amount > customer.approved_limit:
        return {
            'approval': 'rejected',
            'reason': f'Loan amount (${loan.loan_amount:,.2f}) exceeds approved limit (${customer.approved_limit:,.2f})',
            'credit_score': credit_score
        }
    
    # Check debt-to-income ratio
    current_debt = customer.current_debt + loan.loan_amount
    dti_ratio = (current_debt / customer.monthly_salary) * 100
    
    if dti_ratio > 50:
        return {
            'approval': 'rejected',
            'reason': f'Debt-to-income ratio too high ({dti_ratio:.1f}%)',
            'credit_score': credit_score
        }
    
    # Check credit score
    if credit_score < 580:
        return {
            'approval': 'rejected',
            'reason': f'Credit score too low ({credit_score})',
            'credit_score': credit_score
        }
    elif credit_score < 670:
        return {
            'approval': 'pending',
            'reason': f'Credit score requires manual review ({credit_score})',
            'credit_score': credit_score
        }
    else:
        return {
            'approval': 'approved',
            'reason': f'All criteria met. Credit score: {credit_score}',
            'credit_score': credit_score
        }