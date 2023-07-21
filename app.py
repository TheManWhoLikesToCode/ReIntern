##Author: Jaydin F.
##Edited by: Axel C.
##Date: 7/19/2023

from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_behind_proxy import FlaskBehindProxy
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user,logout_user
import git
import threading
from google_calendar_api import main as google_calendar_main, revoke_tokens      ##Import Google Calendar API File 


##Extra python files with their respective 

from forms import RegistrationForm, LoginForm   ##Register and Log in forms 
from models import User                         ##User Model Import


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Add a secret key for security
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Specify the login view route name

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('landing_page.html')

# Routes for registration and login

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('hello'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.email.data}!', 'success')
        login_user(user)
        return redirect(url_for('home'))   ## Change for the results page function

    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))  # Redirect to the homepage

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash(f'Welcome Back {form.email.data}!', 'success')
            return redirect(url_for('hello'))  # Redirect to the homepage
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html', title='Log In', form=form)


@app.route('/calendar')
@login_required
def calendar():
    try:
        google_calendar_main()
    except Exception as e:
        flash(f'Error occurred: {str(e)}', 'danger')
    return redirect(url_for('home'))  # Redirect back to the homepage after fetching and displaying events

@app.route('/calendar_display', methods=['GET', 'POST'])
def calendar_display():
    return render_template('calendar.html')

@app.route("/results", methods=('GET', 'POST'))
def result():
    return render_template('results.html', user='Joe')

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
    app.run(debug=True, host="0.0.0.0")
