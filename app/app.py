from flask import Flask, render_template, redirect, url_for, request, session
import requests
import json
import logging


# Crear el objeto Flask
app = Flask(__name__)
cursor = None
app.secret_key = '1234567'
# Configurar el nivel de log
app.logger.setLevel(logging.DEBUG)


#######################
### PAGINA DE LOGIN ###
#######################

@app.route('/', methods=['POST', 'GET'])
def login():

    msg = ''

    # Mirar si existe algun POST request
    if request.method == 'POST':

        # Crear variables para que sea mas sencillo trabajar con ellas
        username = request.form['username']
        password = request.form['password']

        response = check_user_psswd(username, password)

        if response.get('ok'):
            data = response.get('data')

            # Añadir la informacion a la sesion (accesible desde otras rutas)
            session['loggedin'] = True
            session['id'] = data.get('id')
            session['username'] = data.get('username')
            session['email'] = data.get('email')

            # Redireccionar a la pagina principal
            return redirect(url_for('home'))
        else:
            # Si la cuenta no existe devolver un error
            msg = 'El usuario o la contraseña no son correctos'

    return render_template('login.html', msg=msg)


def check_user_psswd(username, password):

    url = "http://api:5003/check_user_psswd"
    data = {'username': username, 'password': password}
    response = requests.post(url, json=data)

    data = response.json()
    return data


##########################
### SERVICIO DE LOGOUT ###
##########################

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
    # Mirar si existe algun POST request
    if request.method == 'POST':

        # Crear variables para que sea mas sencillo trabajar con ellas
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        response_check = check_user(username)

        
        if response_check.get('ok'):
            if response_check.get('exists'):
                msg = 'La cuenta ya existe, inicia sesión!'
            else:
                response_register = register_user(username, password, email)
                if response_register.get('ok'):
                    msg = 'Te has registrado exitosamente!'
                else:
                    msg = response_register.get('error')
        else:
            msg = 'Ha ocurrido un error, intentalo de nuevo'


    return render_template('registration.html', msg=msg)


def check_user(username):
    data = {'username': username}
    response = requests.post('http://api:5003/check_user', json=data)
    return response.json()


def register_user(username, password, email):
    data = {'username': username, 'password': password, 'email': email}
    response = requests.post('http://api:5003/register_user', json=data)
    return response.json()


###################
### PAGINA HOME ###
###################

@app.route('/home', methods=['GET', 'POST'])
def home():

    # Comprobar si el usuario ha iniciado sesion
    if 'loggedin' in session:

        response = get_public_routes()

        if response.get('ok'):
            public_routes = response.get('data')

        # Si el usuario ha iniciado sesion mostrar el home page
        return render_template('home.html', routes=public_routes)

    # Si el usuario no ha iniciado sesion redireccionar a la pagina de login
    return redirect(url_for('login'))


def get_public_routes():
    response = requests.get('http://api:5003/get_public_routes')
    if response.status_code == 200:
        return response.json()
    else:
        return None

######################
### PAGINA USUARIO ###
######################


@app.route('/profile', methods=['GET', 'POST'])
def profile():

    # Comprobar que el usuario haya iniciado sesion
    if 'loggedin' in session:

        response_user_info = get_user_info(session['username'])

        if response_user_info.get('ok'):

            account = response_user_info.get('data')

        response_user_routes = get_user_routes(session['email'])

        if response_user_routes.get('ok'):

            user_routes = response_user_routes.get('data')

        # Mostrar la pagina del usuario (pasarle la informacion)
        return render_template('profile.html', account=account, routes=user_routes)

    # Si el usuario no ha iniciado sesion redireccionar a la pagina de login
    return redirect(url_for('login'))


def get_user_info(username):
    data = {'username': username}
    response = requests.get('http://api:5003/get_user_info', json=data)
    return response.json()
    

def get_user_routes(email):
    data = {'email': email}
    response = requests.get('http://api:5003/get_user_routes', json=data)
    return response.json()
    
##############################
### SERVICIO ELIMINAR RUTA ###
##############################


@app.route('/delete_route', methods=['POST'])
def delete_route():

    # Comprobar que el usuario haya iniciado sesion y haya pulsado el boton eliminar
    if 'loggedin' in session:
        if request.method == 'POST' and 'route_id' in request.form:

            # Obtener el ID de la ruta a eliminar
            route_id = request.form['route_id']

            delete_route(route_id)

            # Redireccionar al usuario de vuelta a la página de inicio
            return redirect(url_for('profile'))

    # Si el usuario no ha iniciado sesión redireccionar a la pagina de login
    return redirect(url_for('login'))


def delete_route(route_id):
    data = {'route_id': route_id}
    requests.post('http://api:5003/delete_route', json=data)


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

            add_route(nombre, dificultad, distancia, desnivel, link, email)

            return redirect(url_for('profile'))
        return render_template('add_route.html')
    return redirect(url_for('login'))


def add_route(nombre, dificultad, distancia, desnivel, link, email):
    data = {
        'nombre': nombre,
        'dificultad': dificultad,
        'distancia': distancia,
        'desnivel': desnivel,
        'link': link,
        'email': email
    }
    requests.post('http://api:5003/add_route', json=data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
