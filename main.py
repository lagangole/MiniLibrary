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

@app.route('/read/<read_status>')
def render_webpage(read_status):
    status = int(read_status)
    query = "SELECT title, author, description, published_year FROM books WHERE read = ?"
    con = create_connection(DATABASE)
    print(con)
    cur = con.cursor()
    #Query the database
    cur.execute(query, (status,))
    book_list = cur.fetchall()
    con.close()
    print(book_list)
    status_title = status
    if status_title == 1:
        status_title = "Read"
    elif status_title == 0:
        status_title = "Not Read"
    return render_template("webbooks.html", books=book_list, status=status_title)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81)