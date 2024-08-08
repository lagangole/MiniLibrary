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

@app.route('/')
def render_home():
    return render_template("index.html")

@app.route('/titles/<title_read>')
def render_webtitle(title_read):
    query = "SELECT title, description FROM books WHERE read =?"
    name = title_read
    con = create_connection(DATABASE)


    cur = con.cursor()
    #Query the database
    cur.execute(query, (name,))
    title_list = cur.fetchall()
    con.close()
    print(title_list)
    return render_template("read.html", titles=title_list)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81)