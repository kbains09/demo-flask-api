from flask import Flask, request, jsonify, Response
from forex_python.converter import CurrencyRates
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from forex_converter import CurrencyConverter
from prometheus_client import Counter, generate_latest


import logging


app = Flask(__name__)
c = CurrencyRates()

# Configure rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    storage_uri="memory://",  # In-memory storage, you can choose a different one
    default_limits=["5 per minute", "20 per hour"],  # Adjust as needed
)

# Configure logging
logging.basicConfig(filename='api.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define custom metrics
requests_total = Counter('api_requests_total', 'Total number of API requests')
errors_total = Counter('api_errors_total', 'Total number of API errors')

# Endpoints
# Route to convert currency
@app.route('/convert', methods=['GET'])
def convert_currency():
    try:
        from_currency = request.args.get('from')
        to_currency = request.args.get('to')
        amount = float(request.args.get('amount'))

        if not from_currency or not to_currency or not amount:
            return jsonify({"error": "Invalid input"}), 400

        conversion = c.convert(from_currency, to_currency, amount)
        result = {
            "from": from_currency,
            "to": to_currency,
            "amount": amount,
            "converted_amount": conversion,
        }

        logging.info(f"Conversion request: {from_currency} to {to_currency}, Amount: {amount}, Result: {conversion}")

        # Increment the request counter
        requests_total.inc()

        return jsonify(result), 200

    except ValueError as e:
        logging.error(f"ValueError: {str(e)}")
        # Increment the error counter
        errors_total.inc()
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        logging.error(f"Exception: {str(e)}")
        # Increment the error counter
        errors_total.inc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

# Endpoint for Prometheus to scrape metrics
@app.route('/metrics', methods=['GET'])
def prometheus_metrics():
    requests_total.inc()
    return Response(generate_latest(), content_type='text/plain; version=0.0.4; charset=utf-8')

# Add a route for getting a list of supported currencies
@app.route('/currencies', methods=['GET'])
def get_supported_currencies():
    currencies = c.get_currencies()
    currency_symbols = {}  # Dictionary to store currency codes and symbols
    for code, name in currencies.items():
        symbol = c.get_symbol(code)
        currency_symbols[code] = f"{name} ({symbol})"

    return jsonify({"currencies": currency_symbols}), 200

# Error handling for invalid currency codes
@app.errorhandler(ValueError)
def handle_value_error(e):
    return jsonify({"error": "Invalid currency code"}), 400

# Error handling for other exceptions
@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)