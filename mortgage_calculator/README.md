# Mortgage Calculator

A professional web application that calculates mortgage amortization schedules. Built with Flask and modern JavaScript, this calculator provides detailed payment breakdowns and allows for easy export of payment schedules.

## Features

- Calculate monthly mortgage payments
- View detailed amortization schedules
- Export payment schedules to CSV
- Responsive design for mobile and desktop
- Custom domain support through ngrok
- Production-ready with Gunicorn WSGI server

## Prerequisites

- Python 3.7+
- pip (Python package installer)
- ngrok account and authtoken

## Installation

1. Clone the repository:
```bash
git clone https://github.com/russorat/calculators.git
cd calculators/mortgage-calculator
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:

```bash
NGROK_AUTH_TOKEN=your_ngrok_auth_token_here
SECRET_KEY=your_secret_key_here
```

## Running the Application

### Development Mode

To run the application in development mode:

```bash
python run.py
```

The application will be available at:
- Local: http://localhost:5001
- Public: https://mortgage.russellsavage.dev (if ngrok is configured)

### Production Mode

To run the application in production mode using Gunicorn:

```bash
gunicorn -c gunicorn.conf.py "app:create_app()"
```

## Project Structure

```
mortgage_calculator/
├── app/
│   ├── __init__.py          # Flask application factory
│   ├── routes.py            # Application routes
│   ├── calculator.py        # Mortgage calculation logic
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css   # Application styles
│   │   ├── js/
│   │   │   └── calculator.js # Frontend JavaScript
│   │   └── favicon.ico
│   └── templates/
│       └── index.html       # Main application template
├── config.py                # Configuration settings
├── requirements.txt         # Python dependencies
├── run.py                   # Development server script
├── gunicorn.conf.py        # Gunicorn configuration
└── .env                    # Environment variables
```

## Configuration

### Environment Variables

- `NGROK_AUTH_TOKEN`: Your ngrok authentication token
- `SECRET_KEY`: Flask secret key for session management
- `NGROK_DOMAIN`: Your custom ngrok domain (e.g., mortgage.russellsavage.dev)

Create a `.env` file in the project root:
```env
NGROK_AUTH_TOKEN=your_ngrok_auth_token_here
SECRET_KEY=your_secret_key_here
NGROK_DOMAIN=your-ngrok-url.ngrok-free.app
```

### Gunicorn Settings

The application uses Gunicorn in production with the following settings:
- Workers: CPU count * 2 + 1
- Worker Class: gthread
- Threads: 4
- Timeout: 120 seconds
- Port: 5001

## API Endpoints

### GET /calculate_mortgage

Calculate mortgage amortization schedule.

Parameters:
- `principal` (float): Loan amount
- `rate` (float): Annual interest rate (percentage)
- `years` (int): Loan term in years

Example:
```
GET /calculate_mortgage?principal=300000&rate=4.5&years=30
```

Response:
```json
{
  "loan_summary": {
    "loan_amount": 300000.00,
    "annual_interest_rate": 4.5,
    "loan_term_years": 30,
    "monthly_payment": 1520.06,
    "total_interest": 247221.60,
    "total_amount_paid": 547221.60,
    "number_of_payments": 360
  },
  "amortization_schedule": [
    {
      "payment_number": 1,
      "payment_amount": 1520.06,
      "principal_payment": 395.06,
      "interest_payment": 1125.00,
      "remaining_balance": 299604.94
    },
    // ... additional payments ...
  ]
}
```

## Development

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request


## License

Apache 2.0

## Author

Russell Savage

## Acknowledgments

- Flask web framework
- ngrok for tunnel services
- Gunicorn WSGI server