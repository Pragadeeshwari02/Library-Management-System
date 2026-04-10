from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# ---------------- DATABASE CONNECTION ----------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="PragathiRoot2578",
    database="library"
)

cursor = db.cursor()

# ---------------- LOGIN ----------------
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])   # FIXED (important)
def login():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']

        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (name, password)
        )
        user = cursor.fetchone()

        if user:
            return redirect(url_for('home', username=name))
        else:
            return render_template('login.html', error="Invalid credentials")

    return render_template('login.html')


# ---------------- SIGNUP ----------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']

        cursor.execute(
            "INSERT INTO users(username,password) VALUES(%s,%s)",
            (name, password)
        )
        db.commit()

        return redirect(url_for('home', username=name))

    return render_template('signup.html')


# ---------------- HOME ----------------
@app.route('/home')
def home():
    username = request.args.get('username', 'Guest')   # FIXED
    return render_template('home.html', user=username)


# ---------------- ADD BOOK ----------------
@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']

        cursor.execute(
            "INSERT INTO books(title, author) VALUES(%s,%s)",
            (title, author)
        )
        db.commit()

        return redirect(url_for('view_books'))

    return render_template('add_book.html')


# ---------------- VIEW BOOKS ----------------
@app.route('/view')
def view_books():
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    return render_template('view_books.html', books=books)


# ---------------- ISSUE BOOK ----------------
@app.route('/issue', methods=['GET', 'POST'])
def issue_book():
    if request.method == 'POST':
        book_id = request.form['book_id']
        username = request.form['username']
        issue_date = datetime.now().date()

        cursor.execute(
            "INSERT INTO issued_books(book_id, username, issue_date) VALUES(%s,%s,%s)",
            (book_id, username, issue_date)
        )

        cursor.execute(
            "UPDATE books SET available=0 WHERE id=%s",
            (book_id,)
        )

        db.commit()

        return redirect(url_for('view_books'))

    return render_template('issue_book.html')

# ---------------- RETURN BOOK + FINE ----------------
@app.route('/return', methods=['GET', 'POST'])
def return_book():
    if request.method == 'POST':
        book_id = request.form['book_id']
        return_date = datetime.now().date()

        cursor.execute(
            "SELECT issue_date FROM issued_books WHERE book_id=%s",
            (book_id,)
        )
        issue = cursor.fetchone()

        fine = 0

        if issue:
            issue_date = issue[0]
            days = (return_date - issue_date).days

            if days > 7:
                fine = (days - 7) * 10   # ₹10 per day

        cursor.execute("""
            UPDATE issued_books 
            SET return_date=%s, fine=%s 
            WHERE book_id=%s
        """, (return_date, fine, book_id))

        cursor.execute(
            "UPDATE books SET available=1 WHERE id=%s",
            (book_id,)
        )

        db.commit()

        return render_template('fines.html', fine=fine)

    return render_template('return_book.html')


# ---------------- VIEW FINES ----------------
@app.route('/fines')
def fines():
    cursor.execute("SELECT * FROM issued_books WHERE fine > 0")
    data = cursor.fetchall()
    return render_template('fines.html', data=data)

# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)