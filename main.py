from flask import Flask, render_template
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
DATABASE = "books.db"

def create_connection(db_file):
    """
    Creates a connection to the database
    :parameter    db_file - the name of the file
    :returns      connection - a connection to the database
    """
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)
    return None

@app.route('/')
def render_home():
    return render_template("index.html")

@app.route('/read')
def render_read():
    query = "SELECT title, description, published_year FROM books WHERE read = 1"
    con = create_connection(DATABASE)
    print(con)
    cur = con.cursor()
    #Query the database
    cur.execute(query)
    book_list = cur.fetchall()
    con.close()
    print(book_list)
    return render_template("read.html", books=book_list)


@app.route('/not_read')
def render_notread():
    query = "SELECT title, author, description, published_year FROM books WHERE read = 0"
    con = create_connection(DATABASE)
    cur = con.cursor()
    #Query the database
    cur.execute(query)
    book_list = cur.fetchall()
    con.close()
    print(book_list)
    return render_template("not_read.html", books=book_list )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81)