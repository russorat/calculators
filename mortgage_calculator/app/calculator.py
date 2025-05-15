from typing import Dict, List
import math



def calculate_mortgage_amortization(principal: float, annual_rate: float, years: int, payment_schedule: str = 'monthly') -> Dict:
    """
    Calculate mortgage amortization schedule.
    
    Args:
        principal (float): The loan amount
        annual_rate (float): Annual interest rate (as a percentage)
        years (int): Loan term in years
        payment_schedule (str): 'monthly' or 'biweekly'
        
    Returns:
        Dict: Contains loan summary and amortization schedule
    """
    # First calculate the monthly payment amount (this will be the same for both schedules)
    monthly_rate = annual_rate / 100 / 12
    num_monthly_payments = years * 12
    
    # Calculate monthly payment using the standard mortgage formula
    monthly_payment = principal * (monthly_rate * (1 + monthly_rate)**num_monthly_payments) / ((1 + monthly_rate)**num_monthly_payments - 1)
    
    # Initialize variables
    remaining_balance = principal
    total_interest = 0
    amortization_schedule: List[Dict] = []
    
    if payment_schedule == 'monthly':
        # For monthly payments, use the standard calculation
        payment_amount = monthly_payment
        num_payments = num_monthly_payments
        periodic_rate = monthly_rate
        payment_frequency = "Monthly"
    else:
        # For bi-weekly payments, use half the monthly payment but paid 26 times per year
        payment_amount = monthly_payment / 2
        num_payments = years * 26  # 26 payments per year
        periodic_rate = annual_rate / 100 / 26  # Bi-weekly interest rate
        payment_frequency = "Bi-weekly"
    
    # Calculate amortization schedule
    for payment_num in range(1, num_payments + 1):
        # Calculate interest for this period
        if payment_schedule == 'monthly':
            interest_payment = remaining_balance * periodic_rate
        else:
            # For bi-weekly, calculate interest on the shorter period
            interest_payment = remaining_balance * periodic_rate
        
        principal_payment = payment_amount - interest_payment
        
        # Update running totals
        total_interest += interest_payment
        remaining_balance = max(0, remaining_balance - principal_payment)  # Prevent negative balance due to rounding
        
        # Calculate year
        if payment_schedule == 'monthly':
            year = math.ceil(payment_num / 12)
        else:
            year = math.ceil(payment_num / 26)
        
        # Add payment details to schedule
        payment_details = {
            "payment_number": payment_num,
            "payment_amount": round(payment_amount, 2),
            "principal_payment": round(principal_payment, 2),
            "interest_payment": round(interest_payment, 2),
            "remaining_balance": round(remaining_balance, 2),
            "year": year
        }
        amortization_schedule.append(payment_details)
        
        # If balance is paid off, stop the schedule
        if remaining_balance == 0:
            break
    
    # Create response dictionary
    response = {
        "loan_summary": {
            "loan_amount": round(principal, 2),
            "annual_interest_rate": annual_rate,
            "loan_term_years": years,
            "payment_frequency": payment_frequency,
            "monthly_payment": round(monthly_payment, 2),  # Added for reference
            "periodic_payment": round(payment_amount, 2),
            "total_interest": round(total_interest, 2),
            "total_amount_paid": round(principal + total_interest, 2),
            "number_of_payments": len(amortization_schedule)  # Use actual number of payments made
        },
        "amortization_schedule": amortization_schedule
    }
    
    return response
