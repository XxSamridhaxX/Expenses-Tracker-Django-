# 💸 Expense Tracker (Django)

A minimal yet fully functional Expense Tracker built with Django. This app allows users to securely log in, add expenses, filter them by category or date, and visualize spending habits using charts. Features include CSV export, dark mode toggle with light bulb icon, and a user-friendly dashboard.

---

## 🚀 Features

- ✅ User Registration & Email Login
- ✅ Add, Edit, Delete Expenses
- ✅ Filter by Category & Date Range
- ✅ Dashboard with Monthly & Total Summaries
- ✅ Charts (Bar & Donut) via Chart.js
- ✅ Export to CSV (Filtered & Full)
- ✅ Password Change Support
- ✅ Dark Mode Toggle with Light Bulb
- ✅ Mobile-Friendly UI

---

## 🛠 Tech Stack

- Backend: Django
- Frontend: HTML, CSS (Bootstrap), JavaScript
- Database: SQLite
- Charts: Chart.js
- Auth: Django User Authentication

---

## Screenshots
* login:
![Login](https://github.com/user-attachments/assets/33ebf4b8-f6ef-4347-b521-8e389f312a42)


---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/XxSamridhaxX/expense-tracker-django.git
cd expense-tracker-django

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Run the development server
python manage.py runserver


