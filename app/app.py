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
            session['email'] = account['email']
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

        # Consultar la base de datos para obtener las rutas publicas
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM rutas")
        public_routes = cursor.fetchall()

        # Si el usuario ha iniciado sesion mostrar el home page
        return render_template('home.html', routes = public_routes)

    # Si el usuario no ha iniciado sesion redireccionar a la pagina de login
    return redirect(url_for('login'))

######################
### PAGINA USUARIO ###
######################

@app.route('/profile')
def profile():
    # Comprobar que el usuario haya iniciado sesion
    if 'loggedin' in session:

        # Extraer toda la informacion del usuario de la DB
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE id = %s', (session['id'],))
        account = cursor.fetchone()

        # Recoger el email del usuario de la session
        user_email = session['email']

        # Consultar la base de datos para obtener las rutas del usuario
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM rutas WHERE email = %s", (user_email,))
        user_routes = cursor.fetchall()

        # Mostrar la pagina del usuario (pasarle la informacion)
        return render_template('profile.html', account=account, routes=user_routes)

    # Si el usuario no ha iniciado sesion redireccionar a la pagina de login
    return redirect(url_for('login'))

############################
### PAGINA ELIMINAR RUTA ###
############################

@app.route('/delete_route', methods=['POST'])
def delete_route():

    # Comprobar que el usuario haya iniciado sesion y haya pulsado el boton eliminar
    if 'loggedin' in session:
        if request.method == 'POST' and 'route_id' in request.form:

            # Obtener el ID de la ruta a eliminar
            route_id = request.form['route_id']

            # Eliminar la ruta de la DB
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("DELETE FROM rutas WHERE id = %s", (route_id,))
            mysql.connection.commit()

            # Redireccionar al usuario de vuelta a la página de inicio
            return redirect(url_for('profile'))
        
    # Si el usuario no ha iniciado sesión redireccionar a la pagina de login
    return redirect(url_for('login'))


##########################
### PAGINA AÑADIR RUTA ###
##########################

@app.route('/add_route', methods=['GET', 'POST'])
def add_route():

    if 'loggedin' in session:
        if request.method == 'POST':
            
            # Obtener los datos del formulario enviado por el usuario
            nombre = request.form['nombre']
            dificultad = request.form['dificultad']
            distancia = request.form['distancia']
            desnivel = request.form['desnivel']
            link = request.form['link']
            email = session['email']

            # Inserta los datos en la base de datos
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(
                'INSERT INTO rutas (nombre, dificultad, distancia, desnivel, link, email) VALUES (%s, %s, %s, %s, %s, %s)',
                (nombre, dificultad, distancia, desnivel, link, email)
            )
            mysql.connection.commit()

            return redirect(url_for('profile'))
        return render_template('add_route.html')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
