from flask import Flask, render_template, make_response, jsonify, request
import db
import jwt
import config

app = Flask(__name__)

cursor, conn = db.connection(app)

@app.route('/')
def index():
    cursor.execute('SELECT * FROM auth')
    users = cursor.fetchall()
    return render_template('login.html')

if __name__ == '__main__':
    app.debug = config.debug
    app.config['SECRET_KEY'] = config.secret
    app.run(port=config.port)