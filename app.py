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
    if users:
        all_users = []
        for i in users:
            tmp_user = {
                'id': i[0],
                'email': i[1],
                'name': i[2],
                'password': i[3]
            }
            all_users.append(tmp_user)
        return make_response(jsonify(all_users), 200)
    else:
        return make_response(jsonify({'message': 'Its something went wrong'}), 400)

if __name__ == '__main__':
    app.debug = config.debug
    app.config['SECRET_KEY'] = config.secret
    app.run(port=config.port)