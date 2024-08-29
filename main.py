from flask import Flask, render_template, request
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

@app.route('/search', methods=['GET', 'POST'])
def render_search():
    """
    Find all records which contain the search item
    :POST contains the search value
    :returns a rendered page
    """
    search = request.form['search']
    title = "Search for " + search
    query = "SELECT title, description FROM books WHERE " \
            "title LIKE ? OR description LIKE ?"
    search = "%" + search + "%"
    con = create_connection(DATABASE)
    cur = con.cursor()
    cur.execute(query, (search, search))
    tag_list = cur.fetchall()
    con.close()

    return render_template("webbooks.html", books=book_list, status=status_title)


if __name__ == "__main__":
    app.run()