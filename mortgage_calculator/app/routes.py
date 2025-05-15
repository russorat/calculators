from flask import Blueprint, render_template, jsonify, send_from_directory, request
import os
from app.calculator import calculate_mortgage_amortization

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return render_template('index.html')

@bp.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(bp.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

@bp.route('/calculate_mortgage', methods=['GET'])
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

@bp.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "tunnel_url": ngrok.get_tunnels()[0].url() if ngrok.get_tunnels() else None
    })
