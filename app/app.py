from flask import Flask, render_template, redirect, url_for, request, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib

# Crear el objeto Flask
app = Flask(__name__)

# Crear las variables de configuracion
app.secret_key = '1234567'

app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'appDb'

# Inicializar MySQL
mysql = MySQL(app)

#######################
### PAGINA DE LOGIN ###
#######################

@app.route('/', methods=['GET', 'POST'])
def login():

     # Mirar si existe algun POST request donde los campos 'username' y 'password' esten llenos
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:

        # Crear variables para que sea mas sencillo trabajar con ellas
        username = request.form['username']
        password = request.form['password']

        # Hashear contraseñas
        hash = password + app.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest()

        # Comprobar si la cuenta existe en la base de datos
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password,))
        
        # Encontrar el usuario que coincide
        account = cursor.fetchone()

        if account:
            # Añadir la informacion a la sesion (accesible desde otras rutas)
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return 'Logged in successfully!'
        else:
            # Si la cuenta no existe devolver un error
            msg = 'Incorrect username/password!'
        
    return render_template('index.html', msg=msg)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)