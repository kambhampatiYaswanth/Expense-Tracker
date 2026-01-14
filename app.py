from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import date
app = Flask(__name__)
from werkzeug.security import generate_password_hash, check_password_hash
app.secret_key = "supersecretkey"
import datetime

# ---------- DATABASE ----------
def get_db():
    return sqlite3.connect("expenses.db")
def init_db():
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()

    # Users table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # Expenses table (with user_id)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL,
        category TEXT,
        description TEXT,
        date TEXT,
        user_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()
init_db()


# def create_table():
#     conn = get_db()
#     conn.execute("""
#         CREATE TABLE IF NOT EXISTS expenses (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             amount REAL,
#             category TEXT,
#             description TEXT,
#             date TEXT
#         )
#     """)
#     conn.commit()
#     conn.close()

# create_table()

# ---------- ROUTES ----------

from datetime import date
from flask import session

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect("expenses.db")
        cur = conn.cursor()

        try:
            cur.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password)
            )
            conn.commit()
        except:
            return "Username already exists"

        conn.close()
        return redirect("/login")

    return render_template("register.html")
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("expenses.db")
        cur = conn.cursor()

        cur.execute(
            "SELECT id, password FROM users WHERE username=?",
            (username,)
        )
        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user[1], password):
            session["user_id"] = user[0]
            return redirect("/")
        else:
            return "Invalid credentials"

    return render_template("login.html")

@app.route("/daily")
def daily():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    # Today button
    if request.args.get("today"):
        selected_date = datetime.date.today().isoformat()
    else:
        selected_date = request.args.get("date")

    if not selected_date:
        return redirect("/")

    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM expenses
        WHERE user_id = ? AND date = ?
    """, (user_id, selected_date))
    expenses = cur.fetchall()

    cur.execute("""
        SELECT SUM(amount) FROM expenses
        WHERE user_id = ? AND date = ?
    """, (user_id, selected_date))
    total = cur.fetchone()[0] or 0

    conn.close()

    return render_template("index.html", expenses=expenses, total=total)




@app.route("/monthly")
def monthly():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    month = request.args.get("month")  # YYYY-MM

    if not month:
        return redirect("/")

    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM expenses
        WHERE user_id = ? AND substr(date, 1, 7) = ?
    """, (user_id, month))
    expenses = cur.fetchall()

    cur.execute("""
        SELECT SUM(amount) FROM expenses
        WHERE user_id = ? AND substr(date, 1, 7) = ?
    """, (user_id, month))
    total = cur.fetchone()[0] or 0

    conn.close()

    return render_template("index.html", expenses=expenses, total=total)

@app.route("/")
def index():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    conn = sqlite3.connect("expenses.db")
    cur = conn.cursor()

    # ---------- TABLE DATA ----------
    cur.execute("""
        SELECT * FROM expenses
        WHERE user_id = ?
        ORDER BY date DESC
    """, (user_id,))
    expenses = cur.fetchall()

    cur.execute("""
        SELECT SUM(amount) FROM expenses
        WHERE user_id = ?
    """, (user_id,))
    total = cur.fetchone()[0] or 0

    # ---------- DAILY GRAPH ----------
    cur.execute("""
        SELECT date, SUM(amount)
        FROM expenses
        WHERE user_id = ?
        GROUP BY date
        ORDER BY date
    """, (user_id,))
    daily_data = cur.fetchall()

    daily_labels = [row[0] for row in daily_data]
    daily_values = [row[1] for row in daily_data]

    # ---------- MONTHLY GRAPH ----------
    cur.execute("""
        SELECT substr(date, 1, 7), SUM(amount)
        FROM expenses
        WHERE user_id = ?
        GROUP BY substr(date, 1, 7)
        ORDER BY substr(date, 1, 7)
    """, (user_id,))
    monthly_data = cur.fetchall()

    monthly_labels = [row[0] for row in monthly_data]
    monthly_values = [row[1] for row in monthly_data]

    conn.close()

    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        daily_labels=daily_labels,
        daily_values=daily_values,
        monthly_labels=monthly_labels,
        monthly_values=monthly_values
    )





@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/add", methods=["POST"])
def add_expense():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    amount = request.form["amount"]
    category = request.form["category"]
    custom_category = request.form.get("custom_category")

    if category == "Other" and custom_category:
        category = custom_category

    description = request.form["description"]
    date = request.form["date"]

    conn = get_db()
    conn.execute(
        """
        INSERT INTO expenses (amount, category, description, date, user_id)
        VALUES (?, ?, ?, ?, ?)
        """,
        (amount, category, description, date, user_id)
    )
    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/delete/<int:id>")
def delete_expense(id):
    conn = get_db()
    conn.execute("DELETE FROM expenses WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")


@app.route("/edit/<int:id>")
def edit_expense(id):
    conn = get_db()
    expense = conn.execute(
        "SELECT * FROM expenses WHERE id = ?", (id,)
    ).fetchone()
    conn.close()

    return render_template("edit.html", expense=expense)
@app.route("/update/<int:id>", methods=["POST"])
def update_expense(id):
    amount = request.form["amount"]
    category = request.form["category"]
    description = request.form["description"]
    date = request.form["date"]

    conn = get_db()
    conn.execute(
        "UPDATE expenses SET amount=?, category=?, description=?, date=? WHERE id=?",
        (amount, category, description, date, id)
    )
    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/test")
def test():
    return "TEST ROUTE WORKING"


if __name__ == "__main__":
    app.run(debug=True)