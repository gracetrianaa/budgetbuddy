from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL
import os
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

# Assuming you are storing these in-memory for simplicity
total_income = 0
total_expense = 0


app = Flask(__name__, template_folder='templates')

# MySQL configurations
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'db')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'root_password')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'income_expense_db')

mysql = MySQL(app)

def create_transactions_table():
    cur = mysql.connection.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            type VARCHAR(10) NOT NULL,
            amount DECIMAL(10, 2) NOT NULL,
            date DATETIME NOT NULL,
            balance DECIMAL(10, 2) NOT NULL DEFAULT 0.00
        )
    """)
    mysql.connection.commit()
    cur.close()

def reset_global_state():
    global total_income, total_expense
    total_income = 0
    total_expense = 0

with app.app_context():
    create_transactions_table()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_income', methods=['POST'])
def add_income():
    amount = request.json['amount']
    cur = mysql.connection.cursor()
    cur.execute("SELECT balance FROM transactions ORDER BY date DESC LIMIT 1")
    last_balance = cur.fetchone()
    if last_balance:
        new_balance = last_balance[0] + amount
    else:
        new_balance = amount
    cur.execute("INSERT INTO transactions (type, amount, date, balance) VALUES (%s, %s, %s, %s)", ('income', amount, datetime.now(), new_balance))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Income added successfully'})

@app.route('/add_expense', methods=['POST'])
def add_expense():
    amount = request.json['amount']
    cur = mysql.connection.cursor()
    cur.execute("SELECT balance FROM transactions ORDER BY date DESC LIMIT 1")
    last_balance = cur.fetchone()
    if last_balance:
        new_balance = last_balance[0] - amount
    else:
        new_balance = -amount
    cur.execute("INSERT INTO transactions (type, amount, date, balance) VALUES (%s, %s, %s, %s)", ('expense', amount, datetime.now(), new_balance))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Expense added successfully'})

@app.route('/daily_summaries', methods=['GET'])
def daily_summaries():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT 
            date, 
            SUM(CASE WHEN type='income' THEN amount ELSE 0 END) as total_income, 
            SUM(CASE WHEN type='expense' THEN amount ELSE 0 END) as total_expense, 
            MAX(balance) as balance
        FROM transactions 
        GROUP BY date 
        ORDER BY date DESC
    """)
    data = cur.fetchall()
    cur.close()

    daily_summaries = []
    for row in data:
        daily_summaries.append({
            'date': row[0].strftime("%Y-%m-%d %H:%M:%S"),
            'total_income': row[1],
            'total_expense': row[2],
            'balance': row[3]
        })

    return jsonify(daily_summaries)

@app.route('/delete_all', methods=['POST'])
def delete_all_summaries():
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM transactions")
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'All daily summaries deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
