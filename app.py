from flask import Flask, render_template, url_for, flash, redirect, request
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
import git
import threading

app = Flask(__name__)

<<<<<<< HEAD
@app.route('/', methods=['GET', 'POST'])
=======

@app.route('/', methods=['GET', 'POST'])

>>>>>>> origin/main
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('landing_page.html')

<<<<<<< HEAD
=======

>>>>>>> origin/main
@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template('login.html')

<<<<<<< HEAD
=======

@app.route("/register", methods=['GET', 'POST'])
def register():
    return render_template('register.html')


>>>>>>> origin/main
@app.route("/results", methods=('GET', 'POST'))
def result():
    return render_template('results.html')

<<<<<<< HEAD
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
=======

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
>>>>>>> origin/main
