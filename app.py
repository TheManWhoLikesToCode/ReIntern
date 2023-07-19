##Author: Jaydin F.
##Edited by: Axel C.
##Date: 7/19/2023

from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user

##Extra python files with their respective 

from forms import RegistrationForm, LoginForm   ##Register and Log in forms 
from models import User                         ##User Model Import


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Add a secret key for security
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Specify the login view route name

## User Loader to keep track of users
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

## Initial Router
@app.route('/')
def hello():
    return 'Hello World!'


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
        return redirect(url_for('hello'))   ## Change for the results page function

    return render_template('signup.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('hello'))  # Redirect to the homepage

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




if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)