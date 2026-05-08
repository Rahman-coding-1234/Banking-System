from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def db():
    return sqlite3.connect("bank.db")

def create_table():
    conn = db()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        balance REAL DEFAULT 0
    )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return "Banking System Running Successfully!"

@app.route("/create_account", methods=["POST"])
def create_account():
    data = request.json
    name = data["name"]

    conn = db()
    cur = conn.cursor()
    cur.execute("INSERT INTO accounts (name, balance) VALUES (?, ?)", (name, 0))
    conn.commit()
    conn.close()

    return jsonify({"message": "Account created successfully"})

@app.route("/deposit", methods=["POST"])
def deposit():
    data = request.json
    account_id = data["account_id"]
    amount = data["amount"]

    conn = db()
    cur = conn.cursor()
    cur.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, account_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Amount deposited successfully"})

@app.route("/withdraw", methods=["POST"])
def withdraw():
    data = request.json
    account_id = data["account_id"]
    amount = data["amount"]

    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT balance FROM accounts WHERE id = ?", (account_id,))
    result = cur.fetchone()

    if result and result[0] >= amount:
        cur.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, account_id))
        conn.commit()
        message = "Withdrawal successful"
    else:
        message = "Insufficient balance"

    conn.close()
    return jsonify({"message": message})

@app.route("/balance/<int:account_id>")
def balance(account_id):
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT name, balance FROM accounts WHERE id = ?", (account_id,))
    result = cur.fetchone()
    conn.close()

    if result:
        return jsonify({"name": result[0], "balance": result[1]})
    return jsonify({"message": "Account not found"})

if __name__ == "__main__":
    create_table()
    app.run(debug=True)