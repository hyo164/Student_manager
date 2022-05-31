from app import app
from flaskext.mysql import MySQL

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'hieu'
app.config['MYSQL_DATABASE_PASSWORD'] = 'hieu123456'
app.config['MYSQL_DATABASE_DB'] = 'hieutest'
app.config['MYSQL_DATABASE_HOST'] = '192.168.234.192'
app.config['MYSQL_DATABASE_PORT'] = 3306
mysql.init_app(app)
