from flask import Flask, render_template, redirect, url_for, request, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import MySQLdb.cursors
import re
import hashlib

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

    msg = ''
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
        cursor.execute(
            'SELECT * FROM users WHERE username = %s AND password = %s', (username, password,))

        # Encontrar el usuario que coincide
        account = cursor.fetchone()

        if account:
            # Añadir la informacion a la sesion (accesible desde otras rutas)
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Si la cuenta no existe devolver un error
            msg = 'Incorrect username/password!'

    return render_template('login.html', msg=msg)

########################
### PAGINA DE LOGOUT ###
########################


@app.route('/logout')
def logout():

    # Para deslogear a un usuario borrar los datos de la sesion
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)

    # Redireccionar a la pagina de login
    return redirect(url_for('login'))

##########################
### PAGINA DE REGISTRO ###
##########################


@app.route('/register', methods=['GET', 'POST'])
def register():

    msg = ''
    # Mirar si existe algun POST request donde los campos 'username', 'password' y 'email' esten llenos
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:

        # Crear variables para que sea mas sencillo trabajar con ellas
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Comprobar si el usuario ya ha sido registrado previamente
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()

        # Si existe ya una cuenta con esos datos mostrar un error
        if account:
            msg = 'Account already exists!'

        # Comprobar la validez del email
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'

        # Comprobar la validez del nombre
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'

        # Comprobar que todos los campos esten completos
        elif not username or not password or not email:
            msg = 'Please fill out the form!'

        else:
            # Hashear la contraseña
            hash = password + app.secret_key
            hash = hashlib.sha1(hash.encode())
            password = hash.hexdigest()

            # Añadir la nueva cuenta a la DB
            cursor.execute(
                'INSERT INTO users VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'

    elif request.method == 'POST':

        # Mensaje para indicar que el formulario no esta completo
        msg = 'Please fill out the form!'

    return render_template('registration.html', msg=msg)

###################
### PAGINA HOME ###
###################


@app.route('/home')
def home():

    # Comprobar si el usuario ha iniciado sesion
    if 'loggedin' in session:
        # Si el usuario ha iniciado sesion mostrar el home page
        return render_template('home.html', username=session['username'])

    # Si el usuario no ha iniciado sesion redireccionar a la pagina de login
    return redirect(url_for('login'))

######################
### PAGINA USUARIO ###
######################


@app.route('/profile')
def profile():
    # Comprobar que el usuario haya iniciado sesion
    if 'loggedin' in session:

        # Extraertoda la informacion del usuario de la DB
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE id = %s', (session['id'],))
        account = cursor.fetchone()

        # Mostrar la pagina del usuario (pasarle la informacion)
        return render_template('profile.html', account=account)

    # Si el usuario no ha iniciado sesion redireccionar a la pagina de login
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host='0.0.0.0')
