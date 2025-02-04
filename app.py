import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_armstrong(n):
    if not isinstance(n, int):
        return False  # Armstrong check only for integers
    num_str = str(abs(n))  # Use absolute value for Armstrong check
    power = len(num_str)
    return sum(int(digit) ** power for digit in num_str) == abs(n)

def digit_sum(n):
    # Ensure we only calculate digit sum for integers
    if isinstance(n, int):
        return sum(int(digit) for digit in str(abs(n)))  # Use absolute value for digit sum
    return 0  # Return 0 for non-integers

def get_fun_fact(n):
    response = requests.get(f"http://numbersapi.com/{n}")
    if response.status_code == 200:
        return response.text
    return "No fun fact available."

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number = request.args.get('number')

    try:
        # Convert input to float first to handle floating-point numbers
        number = float(number)
        # If it's an integer, convert to int
        if number.is_integer():
            number = int(number)
    except (ValueError, TypeError):
        # Return 400 with the invalid input in the response
        return jsonify({"error": "Invalid input, must be an integer.", "number": number}), 400

    # Classifications
    prime = is_prime(number)
    armstrong = is_armstrong(number)
    properties = []

    if armstrong:
        properties.append("armstrong")
    if number % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")

    # Prepare response
    response = {
        "number": number,
        "is_prime": prime,
        "is_perfect": False,  # Placeholder for future implementation
        "properties": properties,
        "digit_sum": digit_sum(number),
        "fun_fact": get_fun_fact(number)
    }

    return jsonify(response), 200  # Always return 200 for valid numbers

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
