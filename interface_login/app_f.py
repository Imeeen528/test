
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import string
import random
from flask_mail import Mail, Message

# setup
app = Flask(__name__, static_url_path='/static', template_folder='templates')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'testflask22@gmail.com'
app.config['MAIL_PASSWORD'] = 'neotest2022'
mail = Mail(app)

def generate_password(length=12):
    # Generate a random password consisting of lowercase letters and digits
    password = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    return password

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
        
        # send an email with the password and sign-in link
        msg = Message('Welcome !', recipients=[email])
        msg.body = f"Your password is {password}. Click this link to sign in: http://sign_in" #link doesn't work just for testing
        mail.send(msg)
        
        return redirect(url_for('upload_file'))

    return render_template('sign_up.html', message=message)

@app.route('/upload', methods=['GET'])
def upload_file():
    return render_template('upload_file.html')

if __name__ == '__main__':
    app.run(debug=True)




