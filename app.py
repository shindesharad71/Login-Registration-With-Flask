from flask import Flask, render_template, request, Blueprint, flash, g, redirect, session, url_for
import db
import jwt
import config

app = Flask(__name__)

cursor, conn = db.connection(app)

@app.route('/login', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = None
        cursor.execute('SELECT * FROM auth WHERE email=%s', (email))
        user = cursor.fetchone()
        app.logger.debug(user)
        # print(user)
        if user is None:
            error = 'Incorrect username.'
        elif not user[3] == password:
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user[0]
            return redirect(url_for('home'))
        flash(error)
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.debug = config.debug
    app.config['SECRET_KEY'] = config.secret
    app.run(port=config.port)