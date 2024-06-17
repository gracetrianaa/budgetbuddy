from flask import Flask, request, jsonify, render_template

# Assuming you are storing these in-memory for simplicity
total_income = 0
total_expense = 0

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/add_income', methods=['POST'])
    def add_income():
        global total_income
        data = request.get_json()
        amount = data['amount']
        total_income += amount
        return jsonify({"message": "Income added", "total_income": total_income})

    @app.route('/add_expense', methods=['POST'])
    def add_expense():
        global total_expense
        data = request.get_json()
        amount = data['amount']
        total_expense += amount
        return jsonify({"message": "Expense added", "total_expense": total_expense})

    @app.route('/summary', methods=['GET'])
    def summary():
        balance = total_income - total_expense
        return jsonify({
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": balance
        })

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='localhost', port=5000)