from os import name, read
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


def get_titles(title_read):
    """Returns titles and description depending on if it is read"""
    name = int(title_read)
    if name == 1:
        name = "read"
    elif name == 0:
        name = "not read"
    query = "SELECT title, description FROM books WHERE read=?"
    con = create_connection(DATABASE)
    cur = con.cursor()

    # Query the DATABASE
    cur.execute(query, (name,))
    read_list = cur.fetchall()
    
    con.close()
    #print(tag_list)
    return read_list

def get_reads():
    """ Returns the items 1 and 0"""
    con = create_connection(DATABASE)
    query = "SELECT DISTINCT read FROM books"
    #records = run_query(query)
    cur = con.cursor()
    cur.execute(query)
    records = cur.fetchall()
    #print(records)
    for i in range(len(records)):
        records[i] = records[i][0]
    #print(records)
    return records

@app.route('/')
def render_home():
    return render_template('index.html', reads=get_reads())


@app.route('/titles/<title_read>')
def render_webpage(title_read):

    name = int(title_read)
    if name == 1:
        name = "read"
    elif name == 0:
        name = "not read"
    print(name)
    return render_template('libray.html', titles=get_titles(title_read), name=name, reads=get_reads())

@app.route('/sort/<name>')
def render_sortpage(name):
    sort = request.args.get('sort', 'title')
    order = request.args.get('order', 'asc')  # Get the current sort order, default to 'asc' if not provided

    # Toggle the sort order
    if order == 'asc':
        new_order = 'desc'
    else:
        new_order = 'asc'

    # Sort query
    query = "SELECT title, description FROM books WHERE title=? ORDER BY " + sort + " " + order

    con = create_connection(DATABASE)
    cur = con.cursor()

    # Query the DATABASE
    cur.execute(query, (name,))
    title_list = cur.fetchall()
    con.close()

    return render_template('library.html', titles=title_list, name=name, reads=get_reads(), order=new_order)


@app.route('/search', methods=['GET', 'POST'])
def render_search():
    """
    Find all records which contain the search item
    :POST contains the search value
    :returns a rendered page
    """
    search = request.form['search']
    name = "Search for " + search
    query = "SELECT title, description FROM books WHERE " \
            "title LIKE ? OR description LIKE ?"
    search = "%" + search + "%"
    con = create_connection(DATABASE)
    cur = con.cursor()
    cur.execute(query, (search, search))
    title_list = cur.fetchall()
    con.close()

    return render_template("library.html", titles=title_list, name=name, reads=get_reads())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81)
