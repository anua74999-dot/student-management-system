import json
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = "library_secret_key"

BOOKS_FILE = "data/books.json"
MEMBERS_FILE = "data/members.json"
TRANSACTIONS_FILE = "data/transactions.json"

# --- Storage Helpers ---
def load_data(filepath):
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []

def save_data(filepath, data):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

# --- Routes ---

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()

        # Simple admin authentication (replace/extend as needed)
        if username == "admin" and password == "admin123":
            session['user'] = username
            flash("Logged in successfully!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password.", "danger")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("You have been logged out.", "success")
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        flash("Please log in to access the dashboard.", "warning")
        return redirect(url_for('login'))

    books = load_data(BOOKS_FILE)
    members = load_data(MEMBERS_FILE)
    transactions = load_data(TRANSACTIONS_FILE)
    query = request.args.get('search', '').strip().lower()

    if query:
        books = [b for b in books if query in b['title'].lower() or query in b['author'].lower() or query in b['category'].lower()]

    return render_template('dashboard.html', books=books, members=members, transactions=transactions, query=query)

@app.route('/add_book', methods=['POST'])
def add_book():
    if 'user' not in session:
        return redirect(url_for('login'))

    books = load_data(BOOKS_FILE)
    b_id = request.form.get('book_id').strip()
    title = request.form.get('title').strip()
    author = request.form.get('author').strip()
    category = request.form.get('category').strip()
    try:
        copies = int(request.form.get('total_copies'))
    except ValueError:
        flash("Total copies must be a valid number.", "danger")
        return redirect(url_for('dashboard'))

    if any(b['book_id'] == b_id for b in books):
        flash(f"Book ID '{b_id}' already exists!", "danger")
    else:
        new_book = {
            "book_id": b_id,
            "title": title,
            "author": author,
            "category": category,
            "total_copies": copies,
            "available_copies": copies
        }
        books.append(new_book)
        save_data(BOOKS_FILE, books)
        flash("Book added successfully!", "success")

    return redirect(url_for('dashboard'))

@app.route('/add_member', methods=['POST'])
def add_member():
    if 'user' not in session:
        return redirect(url_for('login'))

    members = load_data(MEMBERS_FILE)
    m_id = request.form.get('member_id').strip()
    name = request.form.get('name').strip()
    email = request.form.get('email').strip()

    if any(m['member_id'] == m_id for m in members):
        flash(f"Member ID '{m_id}' already exists!", "danger")
    else:
        members.append({"member_id": m_id, "name": name, "email": email})
        save_data(MEMBERS_FILE, members)
        flash("Member added successfully!", "success")

    return redirect(url_for('dashboard'))

@app.route('/issue_book', methods=['POST'])
def issue_book():
    if 'user' not in session:
        return redirect(url_for('login'))

    m_id = request.form.get('member_id').strip()
    b_id = request.form.get('book_id').strip()

    books = load_data(BOOKS_FILE)
    members = load_data(MEMBERS_FILE)
    transactions = load_data(TRANSACTIONS_FILE)

    book = next((b for b in books if b['book_id'] == b_id), None)
    member = next((m for m in members if m['member_id'] == m_id), None)

    if not member:
        flash(f"Member ID '{m_id}' not found.", "danger")
    elif not book:
        flash(f"Book ID '{b_id}' not found.", "danger")
    elif book['available_copies'] <= 0:
        flash(f"No copies available for '{book['title']}'.", "danger")
    elif any(t for t in transactions if t['member_id'] == m_id and t['book_id'] == b_id and t['return_date'] is None):
        flash("Member already holds an unreturned copy of this book.", "warning")
    else:
        book['available_copies'] -= 1
        txn_id = f"T{len(transactions) + 1:04d}"
        transactions.append({
            "transaction_id": txn_id,
            "member_id": m_id,
            "book_id": b_id,
            "issue_date": datetime.today().strftime('%Y-%m-%d'),
            "return_date": None
        })
        save_data(BOOKS_FILE, books)
        save_data(TRANSACTIONS_FILE, transactions)
        flash(f"Book '{book['title']}' issued successfully!", "success")

    return redirect(url_for('dashboard'))

@app.route('/return_book', methods=['POST'])
def return_book():
    if 'user' not in session:
        return redirect(url_for('login'))

    m_id = request.form.get('member_id').strip()
    b_id = request.form.get('book_id').strip()

    books = load_data(BOOKS_FILE)
    transactions = load_data(TRANSACTIONS_FILE)

    txn = next((t for t in transactions if t['member_id'] == m_id and t['book_id'] == b_id and t['return_date'] is None), None)

    if not txn:
        flash("No active issue record found for this Member and Book combination.", "danger")
    else:
        txn['return_date'] = datetime.today().strftime('%Y-%m-%d')
        book = next((b for b in books if b['book_id'] == b_id), None)
        if book:
            book['available_copies'] += 1
            save_data(BOOKS_FILE, books)
        save_data(TRANSACTIONS_FILE, transactions)
        flash("Book returned successfully!", "success")

    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)