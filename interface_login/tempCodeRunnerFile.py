from flask_mail import Mail, Message
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import string
import random
import os

# setup
app = Flask(__name__, static_url_path='/static', template_folder='templates')
# Instantiate Mail
mail = Mail(app)


def generate_password(length=12):
    # Generate a random password consisting of lowercase letters and digits
    password = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    return password




# set up Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')




@app.route('/', methods=['GET', 'POST'])
def sign_up():
    message = ''

    if request.method == 'POST':

        # SQLite
        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        # HTML form
        name = request.form['username']
        password = generate_password()
        email = request.form['email']
        print(name, password, email)

        # insert user into the database
        insert_query = "INSERT INTO users (name, password, email) VALUES (?, ?, ?)"
        values = (name, password, email)
        cursor.execute(insert_query, values)
        connection.commit()
        user = cursor.fetchone()
        
        # Send email
        msg = Message('Welcome to My App', recipients=[email])
        msg.body = f"Your password is: {password}"
        mail.send(msg)

        return redirect(url_for('upload_file'))

    return render_template('sign_up.html', message=message)


