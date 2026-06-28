from flask import Flask, request, jsonify

app = Flask(__name__)

expense_data = []
total = 0

@app.route('/')
def home():
    return "Welcome to the Expense Tracker API!"

@app.route('/expense')
def expense():
    return jsonify({"expense":expense_data, "total":total}), 200

@app.route('/expense', methods=['POST'])
def add_expense():
    data = request.get_json()
    if data is None or data.get('name') is None or data.get('price') is None:
        return jsonify({"error": "Invalid input"}), 400
    
    name = data.get('name')
    price = data.get('price')

    try:
        price = float(price)
    except (TypeError, ValueError):
        return jsonify({"error": "Price must be a number"}), 400

    if not name or price < 0:
        return jsonify({"error": "Invalid expense data"}), 400

    new_expense = {
        "name": name,
        "price": price
    }
    global total
    total += price
    expense_data.append(new_expense)

    return jsonify({"expense": new_expense, "total": total}), 201

@app.route('/total')
def get_total():
    return jsonify({"total": total}), 200

if __name__ == "__main__":
    app.run(debug=True)