from flask import Flask, render_template, url_for, flash, redirect, request, session
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
import git
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('landing_page.html')


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
            return render_template('results.html')
        else:
            flash('Incorrect email / password !')
            print("Login failed")  # Added print statement
    return render_template('login.html')


@app.route("/logout")
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('name', None)
    return redirect(url_for('login'))


@app.route("/register", methods=['GET', 'POST'])
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


@app.route("/results", methods=('GET', 'POST'))
def result():
    return render_template('results.html')


@app.route("/admin", methods=['GET', 'POST'])
def admin():
    if 'loggedin' in session and session['email'] == 'user@admin.com':
        users = User.query.all()
        return render_template('admin.html', users=users)
    else:
        return redirect(url_for('login'))


@app.route("/print_users", methods=['GET'])
def print_users():
    users = User.query.all()
    for user in users:
        print(f"User ID: {user.id}, Name: {user.name}, Email: {user.email}")
    return "Users printed in console"


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


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0")
