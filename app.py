##Author: Jaydin F.
##Edited by: Axel C.
##Date: 7/19/2023

from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_behind_proxy import FlaskBehindProxy
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user,logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from prompt import generate_brag_sheet
from flask import jsonify
import git
import threading
import logging


##Extra python files with their respective 

from forms import RegistrationForm, LoginForm   ##Register and Log in forms 
from models import User                         ##User Model Import


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Specify the login view route name
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        logging.info("POST request received at /home route.")
        summary = request.get_json().get('summary', '')
        logging.info(f"Summary received: {summary}")
        if 'loggedin' in session:
            name = session['name']
            logging.info(f"User {name} is logged in.")
            brag_sheet_bullets = generate_brag_sheet(summary, name)
            session['brag_sheet_bullets'] = brag_sheet_bullets
            logging.info(f"Brag sheet bullets generated: {brag_sheet_bullets}")
            return jsonify({'brag_sheet_bullets': brag_sheet_bullets})
        else:
            logging.info("User not logged in. Redirecting to login page.")
            return redirect(url_for('login'))
    logging.info("GET request received at /home route.")
    return render_template('landing_page.html')

# Routes for registration and login

#   @app.route('/register', methods=['GET', 'POST'])
#   def register():
#       if current_user.is_authenticated:
#           return redirect(url_for('hello'))
#
#       form = RegistrationForm()
#       if form.validate_on_submit():
#           user = User(email=form.email.data, password=form.password.data)
#           db.session.add(user)
#           db.session.commit()
#           flash(f'Account created for {form.email.data}!', 'success')
#           login_user(user)
#           return redirect(url_for('home'))   ## Change for the results page function
#
#       return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # Added print statement
        print(f"Attempting to login with email: {email}")
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['loggedin'] = True
            session['id'] = user.id
            session['name'] = user.name
            session['email'] = email  # Add this line
            print("Login successful")  # Added print statement
            return render_template('index.html')
        else:
            flash('Incorrect email / password !')
            print("Login failed")  # Added print statement
    return render_template('login.html')


@app.route("/logout", methods=['POST'])
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('name', None)
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        password = generate_password_hash(
            request.form.get('password'), method='sha256')
        email = request.form.get('email')
        # Added print statement
        print(f"Attempting to register with email: {email}, name: {name}")
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists !')
            # Added print statement
            print("Registration failed, email already exists")
        else:
            new_user = User(name=name, password=password, email=email)
            db.session.add(new_user)
            db.session.commit()
            flash('You have successfully registered !')
            print("Registration successful")  # Added print statement
            return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/calendar_display', methods=['GET', 'POST'])
def calendar_display():
    return render_template('calendar.html')


@app.route("/index", methods=('GET', 'POST'))
def result():
    if 'loggedin' in session:
        name = session['name']
        brag_sheet_bullets = session.get('brag_sheet_bullets', [])
        return render_template('index.html', name=name, brag_sheet_bullets=brag_sheet_bullets)
    else:
        return redirect(url_for('login'))


@app.route("/admin", methods=['GET', 'POST'])
def admin():
    if 'loggedin' in session and session['email'] == 'user@admin.com':
        users = User.query.all()
        return render_template('admin.html', users=users)
    else:
        return redirect(url_for('login'))


@app.route('/edit_user/<int:id>', methods=['POST'])
def edit_user(id):
    data = request.get_json()
    user = User.query.get(id)
    # update user details
    user.name = data.get('name')
    user.email = data.get('email')
    # save changes
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})


@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin'))


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')


@app.route('/wiki', methods=['GET', 'POST'])
def wiki():
    return render_template('wiki.html')


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    return render_template('settings.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0")
