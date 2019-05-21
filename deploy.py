import sqlite3, os
from flask import Flask, render_template, request, redirect
from flask_sslify import SSLify
from hash import get_link, add_link


curdir = os.getcwd()
datafile = f"{curdir}/links.db"
indexfile = 'index.html'
URL = "https://evo-linker.herokuapp.com/"

app = Flask(__name__)
sslify = SSLify(app)


# cursor.execute('CREATE TABLE links (origin text, hash text)')


@app.route('/None', methods=['GET'])
def redirect_none():
    return "<h2>404 Not Found</h2>"


@app.route('/<hashed>', methods=['GET'])
def redirect_origin(hashed):
    conn = sqlite3.connect(datafile)
    cursor = conn.cursor()
    link = get_link(cursor, hashed)
    cursor.close()
    conn.close()
    return redirect(link, code=302)


@app.route('/', methods=['POST'])
def getvalue():
    conn = sqlite3.connect(datafile)
    cursor = conn.cursor()

    link = request.form['link']
    hashed = add_link(cursor, link)
    hashedLink = f"{URL}{hashed}"

    conn.commit()
    cursor.close()
    conn.close()
    return render_template(indexfile, link=hashedLink)


@app.route('/')
def index():
    return render_template(indexfile)


if __name__ == '__main__':
    app.run(debug=True)