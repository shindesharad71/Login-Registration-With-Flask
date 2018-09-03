from flaskext.mysql import MySQL
import config

def connection(app):
    mysql = MySQL()
    app.config['MYSQL_DATABASE_USER'] = config.dbuser
    app.config['MYSQL_DATABASE_PASSWORD'] = config.dbpassword
    app.config['MYSQL_DATABASE_DB'] = config.dbname
    app.config['MYSQL_DATABASE_HOST'] = config.dbhost
    mysql.init_app(app)
    conn = mysql.connect()
    cursor = conn.cursor()
    return cursor, conn