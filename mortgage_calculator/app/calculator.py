from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from typing import Dict, List
import math
import os
import ngrok
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

def setup_ngrok():
    try:
        # Configure ngrok with your auth token
        listener = ngrok.forward(
            "localhost:5001",
            authtoken=os.getenv('NGROK_AUTH_TOKEN'),
            domain="mortgage.russellsavage.dev"
        )
        logger.info(f"ngrok tunnel established at: {listener.url()}")
        
    except Exception as e:
        logger.error(f"Error setting up ngrok: {str(e)}")
        raise

def cleanup_ngrok():
    try:
        ngrok.disconnect()
        logger.info("Disconnected ngrok tunnel")
    except Exception as e:
        logger.error(f"Error disconnecting ngrok tunnel: {str(e)}")

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

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate_mortgage', methods=['GET'])
def get_mortgage_calculation():
    try:
        # Get parameters from query string
        principal = float(request.args.get('principal', 0))
        annual_rate = float(request.args.get('rate', 0))
        years = int(request.args.get('years', 0))
        payment_schedule = request.args.get('paymentSchedule', 'monthly')
        
        # Validate input
        if principal <= 0 or annual_rate <= 0 or years <= 0:
            return jsonify({
                "error": "Invalid input parameters. All values must be positive numbers."
            }), 400
            
        if payment_schedule not in ['monthly', 'biweekly']:
            return jsonify({
                "error": "Invalid payment schedule. Must be 'monthly' or 'biweekly'."
            }), 400
            
        # Calculate amortization schedule
        result = calculate_mortgage_amortization(principal, annual_rate, years, payment_schedule)
        return jsonify(result)
        
    except (TypeError, ValueError) as e:
        return jsonify({
            "error": "Invalid input parameters. Please check the data types and try again.",
            "details": str(e)
        }), 400

# Add route for favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "tunnel_url": ngrok.get_tunnels()[0].url() if ngrok.get_tunnels() else None
    })

if __name__ == '__main__':
    # Set up ngrok before starting the Flask app
    setup_ngrok()
    
    try:
        # Run the Flask app
        app.run(debug=True, port=5001)
    finally:
        # Clean up ngrok when the app stops
        cleanup_ngrok()
