from flask import Flask, request, jsonify
from forex_python.converter import CurrencyRates

app = Flask(__name__)
c = CurrencyRates()

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

        return jsonify(result), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

# Add a route for getting a list of supported currencies
@app.route('/currencies', methods=['GET'])
def get_supported_currencies():
    currencies = c.get_currencies()
    return jsonify({"currencies": currencies}), 200

# Error handling for invalid currency codes
@app.errorhandler(ValueError)
def handle_value_error(e):
    return jsonify({"error": "Invalid currency code"}), 400

# Error handling for other exceptions
@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)