from flask import Flask, render_template, request, Blueprint, flash, g, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import db
import jwt
import config
import hashlib

app = Flask(__name__)

cursor, conn = db.connection(app)


@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'GET':
        if 'user_id' in session:
            app.logger.debug(session['user_id'])
            return redirect(url_for('home'))
        return render_template('login.html')
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = None
        cursor.execute('SELECT * FROM auth WHERE email=%s', (email))
        user = cursor.fetchone()
        app.logger.debug(user)
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user[3], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user[0]
            return redirect(url_for('home'))
        flash(error)
        return render_template('login.html', title='Login')

@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'GET':
        if 'user_id' in session:
            app.logger.debug(session['user_id'])
            return redirect(url_for('home'))
        return render_template('register.html', title='Register')
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']
        error = None
        if password != confirm:
            error = 'password and confirm password does not match'
        else:
            cursor.execute('SELECT * FROM auth WHERE email=%s', (email))
            user = cursor.fetchone()
            app.logger.debug(user)
            if user:
                error = 'Sorry, email already exist!'

        if error is None:
            password = generate_password_hash(password)
            cursor.execute('INSERT into auth (name, email, password) VALUES (%s,%s,%s)', (name, email, password))
            user = cursor.fetchone()
            conn.commit()
            if cursor.lastrowid:
                flash('Registration successfull!, login now!')
                return redirect(url_for('login'))
            else:
                flash('Something went wrong, try again!')
                return render_template('register.html', title='Register')
        flash(error)
        return render_template('register.html', title='Register')

@app.route('/')
def index():
    if request.method == 'GET':
        if 'user_id' in session:
            return redirect(url_for('home'))
    return redirect(url_for('login'))


@app.route('/home')
def home():
    if request.method == 'GET':
        if 'user_id' not in session:
            return redirect(url_for('login'))
    cursor.execute('SELECT * FROM auth WHERE id=%s', (session['user_id']))
    user = cursor.fetchone()
    name = user[2]
    return render_template('home.html', title=name, name=name)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have successfully logged out.')
    return redirect('/login')


if __name__ == '__main__':
    app.debug = config.debug
    app.config['SECRET_KEY'] = config.secret
    app.run(port=config.port)
