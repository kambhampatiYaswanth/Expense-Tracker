# 🚀 Expense Tracker Web Application (Flask)

A full-stack **Expense Tracker** web application built using **Flask (Python)** and **SQLite** that helps users track, analyze, and manage their daily and monthly expenses with authentication and visual analytics.

---

## 📌 Project Overview

Managing personal expenses is difficult without proper tracking and insights.  
This project provides a simple yet powerful solution where users can:

- Securely log in
- Add and categorize expenses
- View daily and monthly summaries
- Analyze spending patterns using charts

This project follows **MVC principles**, **RESTful routing**, and **clean UX design**, making it suitable for real-world use and technical interviews.

---

## ✨ Features

### 🔐 Authentication
- User Registration
- User Login
- Secure password hashing
- Logout functionality

### 💰 Expense Management
- Add expenses with:
  - Amount
  - Category
  - Custom category option
  - Description
  - Date
- Edit existing expenses
- Delete expenses

### 📅 Filters & Views
- View **all expenses**
- Filter expenses by:
  - Daily
  - Monthly
- One-click **Today** option

### 📊 Expense Analysis
- Daily expense trend graph
- Monthly expense summary graph
- Charts generated using **Chart.js**
- Analysis section shown only when requested

### 🎨 UI / UX
- Clean and responsive UI
- Separate pages for login, register, dashboard, and edit
- Dynamic UI interactions using JavaScript
- User-friendly navigation

---

## 🛠 Tech Stack

### Backend
- Python
- Flask
- SQLite
- Werkzeug Security

### Frontend
- HTML5
- CSS3
- JavaScript
- Chart.js

### Tools
- Git & GitHub
- VS Code

---

## 🗂 Project Structure
expense_tracker/
│
├── app.py
├── expenses.db
├── .gitignore
├── README.md
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── index.html
│   ├── edit.html
│
├── static/
│   ├── style.css
│
├── screenshots/
│   ├── login.png
│   ├── register.png
│   ├── dashboard.png
│   ├── analysis.png


---

## 🧠 Core Concepts Used

- RESTful routing
- MVC architecture
- Template rendering using Jinja2
- Session-based authentication
- SQL queries
- DOM manipulation
- Event handling
- Data visualization

---

## ▶️ How to Run Locally
git clone https://github.com/YOUR_USERNAME/expense-tracker-flask.git
cd expense-tracker-flask
python -m venv venv
venv\Scripts\activate
pip install flask
python app.py
