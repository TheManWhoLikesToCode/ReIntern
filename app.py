# Author: Jaydin F.
# Edited by: Axel C.
# Date: 7/19/2023

from flask import Flask, render_template, redirect, url_for, flash, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from prompt import generate_brag_sheet, generate_weekly_email
import logging
from days_until import calculate_days_until_friday
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    task = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False)
    user = db.relationship('User', backref=db.backref('tasks', lazy=True))


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        logging.info("POST request received at /home route.")
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')
        if not start_date_str or not end_date_str:
            return jsonify({'message': 'Please provide a start and end date for the summary'}), 400
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        if 'loggedin' in session:
            user_id = session['id']
            name = session['name']
            logging.info(f"User {name} is logged in.")
            tasks = Task.query.filter(
                Task.user_id == user_id, Task.date.between(start_date, end_date)).all()
            task_text = ' '.join([task.task for task in tasks])
            # Print the tasks being sent to the prompt
            print(f"Sending the following tasks to the prompt: {task_text}")
            brag_sheet_bullets = generate_brag_sheet(task_text, name)
            session['brag_sheet_bullets'] = brag_sheet_bullets
            logging.info(f"Brag sheet bullets generated: {brag_sheet_bullets}")
            return jsonify({'brag_sheet_bullets': brag_sheet_bullets})
        else:
            logging.info("User not logged in. Redirecting to login page.")
            return redirect(url_for('login'))
    logging.info("GET request received at /home route.")
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


@app.route('/add_event', methods=['POST'])
def add_event():
    try:
        data = request.get_json()
        title = data.get('title')
        start_str = data.get('start')
        end_str = data.get('end')

        if not title or not start_str or not end_str:
            return jsonify({'message': 'Event data is incomplete'}), 400

        # Parse the date and time strings into Python datetime objects
        start = datetime.fromisoformat(start_str)
        end = datetime.fromisoformat(end_str)

        # Check if the user is logged in
        if 'loggedin' in session:
            user_id = session['id']

            # Create a new event entry in the database associated with the user
            new_event = Event(title=title, start_date=start,
                              end_date=end, user_id=user_id)
            db.session.add(new_event)
            db.session.commit()

            return jsonify({'message': 'Event added successfully'})
        else:
            return jsonify({'error': 'User not logged in'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/get_events', methods=['GET'])
def get_events():
    # Check if the user is logged in
    if 'loggedin' in session:
        user_id = session['id']

        # Query the events associated with the user
        events = Event.query.filter_by(user_id=user_id).all()

        event_list = []
        for event in events:
            event_list.append({
                'title': event.title,
                'start': event.start_date.strftime('%Y-%m-%d %H:%M:%S'),
                'end': event.end_date.strftime('%Y-%m-%d %H:%M:%S')
            })
        return jsonify(event_list)
    else:
        return jsonify({'error': 'User not logged in'})


@app.route('/generate_email', methods=['POST'])
def generate_email():
    if 'loggedin' in session:
        # Get the current week's start and end dates
        current_week_start = datetime.now().date(
        ) - timedelta(days=datetime.now().weekday())
        current_week_end = current_week_start + timedelta(days=6)

        # Query the database for tasks in the current week for the logged in user
        tasks = Task.query.filter(Task.user_id == session['id'], Task.date.between(
            current_week_start, current_week_end)).all()

        # Now you have the tasks for the current week for the logged in user
        print(f"Current week tasks: {tasks}")

        # Convert tasks to a list of dictionaries to match the format expected by generate_weekly_email
        tasks_list = [{'task': task.task, 'date': task.date} for task in tasks]

        # Generate the email content based on the tasks
        email_content = generate_weekly_email(
            tasks_list, session['name'])

        # Return the email content
        return jsonify({'email_content': email_content})

    else:
        return jsonify({'error': 'User not logged in'})


@app.route("/generateSummary", methods=['POST'])
def generateSummary():
    if 'loggedin' in session:
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')
        if not start_date_str or not end_date_str:
            return jsonify({'message': 'Please provide a start and end date for the summary'}), 400
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        user_id = session['id']
        tasks = Task.query.filter(
            Task.user_id == user_id, Task.date.between(start_date, end_date)).all()
        task_text = ' '.join([task.task for task in tasks])
        print(f"Sending the following tasks to the prompt: {task_text}")
        summary_result = generate_brag_sheet(task_text, session['name'])
        return jsonify({'summary_result': summary_result})
    else:
        return redirect(url_for('login'))


@app.route("/index", methods=('GET', 'POST'))
def result():
    if 'loggedin' in session:
        name = session['name']
        user_id = session['id']

        # Retrieve tasks from the database for the logged-in user
        tasks = Task.query.filter_by(user_id=user_id).all()

        # Calculate days until Friday
        days_until_friday = calculate_days_until_friday()

        # Pass the tasks and days_until_friday to the template
        return render_template('index.html', name=name, tasks=tasks, days_until_friday=days_until_friday)
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


@app.route("/addTask", methods=['POST'])
def addTask():
    if 'loggedin' in session:
        task = request.form.get('task')
        date_str = request.form.get('date')
        if not task:
            return jsonify({'message': 'Please provide a task'}), 400
        if not date_str:
            return jsonify({'message': 'Please provide a due date for the task'}), 400
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        user_id = session['id']
        new_task = Task(task=task, date=date, user_id=user_id)
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'message': 'Task added successfully'})
    else:
        return redirect(url_for('login'))


@app.route('/deleteTask/<int:task_id>', methods=['POST'])
def deleteTask(task_id):
    if 'loggedin' in session:
        task = Task.query.get(task_id)
        if task and task.user_id == session['id']:
            db.session.delete(task)
            db.session.commit()
            return jsonify({'message': 'Task deleted successfully'})
        else:
            return jsonify({'message': 'Task not found'}), 404
    else:
        return redirect(url_for('login'))


@app.route('/wiki', methods=['GET', 'POST'])
def wiki():
    return render_template('wiki.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'loggedin' in session:
        user_id = session['id']
        tasks = Task.query.filter_by(user_id=user_id).all()
        return render_template('dashboard.html', tasks=tasks)
    else:
        return redirect(url_for('login'))


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    return render_template('settings.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=3000)
