from flask import Flask, render_template, url_for, flash, redirect, request, session
from flask_behind_proxy import FlaskBehindProxy
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
from prompt import generate_brag_sheet, generate_weekly_email
import logging
from datetime import datetime, timedelta


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)


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
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')
        if not start_date_str or not end_date_str:
            flash('Please provide a start and end date for the summary')
            return redirect(url_for('home')), 400
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        if 'loggedin' in session:
            user_id = session['id']
            name = session['name']
            flash(f"User {name} is logged in.")
            tasks = Task.query.filter(
                Task.user_id == user_id, Task.date.between(start_date, end_date)).all()
            task_text = ' '.join([task.task for task in tasks])
            flash(f"Sending the following tasks to the prompt: {task_text}")
            brag_sheet_bullets = generate_brag_sheet(task_text, name)
            session['brag_sheet_bullets'] = brag_sheet_bullets
            flash(f"Brag sheet bullets generated: {brag_sheet_bullets}")
            return jsonify({'brag_sheet_bullets': brag_sheet_bullets})
        else:
            flash("User not logged in. Redirecting to login page.")
            return redirect(url_for('login'))
    return render_template('landing_page.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['loggedin'] = True
            session['id'] = user.id
            session['name'] = user.name
            session['email'] = email
            return redirect(url_for('result'))  # Redirect to /index route
        else:
            flash('Incorrect email / password !')
    return render_template('login.html')


@app.route("/logout", methods=['POST'])
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('name', None)
    flash("Logged out successfully.")
    return redirect(url_for('home'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        password = generate_password_hash(
            request.form.get('password'), method='sha256')
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists !')
        else:
            new_user = User(name=name, password=password, email=email)
            db.session.add(new_user)
            db.session.commit()
            flash('You have successfully registered !')
            return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/calendar_display', methods=['GET', 'POST'])
def calendar_display():
    return render_template('calendar.html')


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

        # Convert tasks to a list of dictionaries to match the format expected by generate_weekly_email
        tasks_list = [{'task': task.task, 'date': task.date} for task in tasks]

        # Generate the email content based on the tasks
        email_content = generate_weekly_email(
            tasks_list, session['name'])

        # Return the email content
        return jsonify({'email_content': email_content})

    else:
        flash("User not logged in.")
        return redirect(url_for('login'))


@app.route("/generateSummary", methods=['POST'])
def generateSummary():
    if 'loggedin' in session:
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')
        if not start_date_str or not end_date_str:
            flash('Please provide a start and end date for the summary')
            return redirect(url_for('home')), 400
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        user_id = session['id']
        tasks = Task.query.filter(
            Task.user_id == user_id, Task.date.between(start_date, end_date)).all()
        task_text = ' '.join([task.task for task in tasks])
        summary_result = generate_brag_sheet(task_text, session['name'])
        return jsonify({'summary_result': summary_result})
    else:
        flash("User not logged in.")
        return redirect(url_for('login'))


@app.route("/index", methods=('GET', 'POST'))
def result():
    if 'loggedin' in session:
        name = session['name']
        user_id = session['id']

        # Get today's date
        today = datetime.today()

        # Calculate the number of days until next Friday
        days_until_friday = (4 - today.weekday() + 7) % 7

        # Retrieve tasks from the database for the logged-in user
        tasks = Task.query.filter_by(user_id=user_id).all()

        # Pass the tasks and the countdown to the template
        return render_template('index.html', name=name, tasks=tasks, days_until_friday=days_until_friday)
    else:
        flash("User not logged in.")
        return redirect(url_for('login'))


@app.route("/admin", methods=['GET', 'POST'])
def admin():
    if 'loggedin' in session and session['email'] == 'user@admin.com':
        users = User.query.all()
        return render_template('admin.html', users=users)
    else:
        flash("User not logged in or not an admin.")
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
    flash("User updated successfully.")
    return jsonify({'message': 'User updated successfully'})


@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    flash("User deleted successfully.")
    return redirect(url_for('admin'))


@app.route("/addTask", methods=['POST'])
def addTask():
    if 'loggedin' in session:
        task = request.form.get('task')
        date_str = request.form.get('date')
        if not task:
            flash('Please provide a task')
            return redirect(url_for('home')), 400
        if not date_str:
            flash('Please provide a date for the task')
            return redirect(url_for('home')), 400
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        user_id = session['id']
        new_task = Task(task=task, date=date, user_id=user_id)
        db.session.add(new_task)
        db.session.commit()
        flash("Task added successfully.")
        return jsonify({'message': 'Task added successfully'})
    else:
        flash("User not logged in.")
        return redirect(url_for('login'))


@app.route('/deleteTask/<int:task_id>', methods=['POST'])
def deleteTask(task_id):
    if 'loggedin' in session:
        task = Task.query.get(task_id)
        if task and task.user_id == session['id']:
            db.session.delete(task)
            db.session.commit()
            flash("Task deleted successfully.")
            return jsonify({'message': 'Task deleted successfully'})
        else:
            flash("Task not found.")
            return jsonify({'message': 'Task not found'}), 404
    else:
        flash("User not logged in.")
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
        flash("User not logged in.")
        return redirect(url_for('login'))


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    return render_template('settings.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0")
