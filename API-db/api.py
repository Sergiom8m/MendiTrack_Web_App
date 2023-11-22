from flask import Flask, request
from config import SECRET_APP_KEY, MYSQL_PASSWORD
from flask_mysqldb import MySQL
import MySQLdb.cursors
import MySQLdb.cursors
import hashlib

# Crear y configurar la app
app = Flask(__name__)
app.secret_key = SECRET_APP_KEY

# Configurar la conexion a la base de datos
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = MYSQL_PASSWORD
app.config['MYSQL_DB'] = 'appDb'

mysql = MySQL(app)


# Funcion para hashear contraseñas
def hash_passw(password):
    hash = password + app.secret_key
    hash = hashlib.sha384(hash.encode())
    password = hash.hexdigest()
    return password


@app.route('/check_user_psswd', methods=['POST'])
def check_user_psswd():

    # Inicializar el JSON de respuesta
    response = {'ok': False, 'data':None, 'error':''}

    # Recoger los datos de la peticion
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Hashear contraseña
    password = hash_passw(password)

    try:
    # Comprobar si la cuenta existe en la DB
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password,))
        account = cursor.fetchone()

        # Si la cuenta existe añadir al JSON los datos del usuario
        if account:
            response['ok'] = True
            response['data'] = {
                'id': account['id'],
                'email': account['email'],
                'username': account['username']
            }
        else:
            response['error'] = 'El usuario no existe'
    
    except Exception as e:

        response['error'] = str(e)

    finally:
        cursor.close()

    return response


@app.route('/check_user_email', methods=['POST'])
def check_user_email():

    # Inicializar el JSON de respuesta
    response = {'ok': True, 'exist': False, 'error':''}

    # Recoger los datos de la peticion
    data = request.json
    username = data.get('username')
    email = data.get('email')

    try:
        # Comprobar si el usuario ya ha sido registrado previamente
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s OR email = %s', (username, email,))
        account = cursor.fetchone()

        # Actualizar el JSON con la infromacion de la existencia del usuario
        if account:
            response['exists'] = True
        else:
            response['exists'] = False

    except Exception as e:
        response['error'] = str(e)
        response['ok'] = False

    finally:
        cursor.close()
        
    return response

@app.route('/register_user', methods=['POST'])
def register_user():

    # Inicializar el JSON de respuesta
    response = {'ok': True, 'error':''}

    # Recoger los datos de la peticion
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    # Hashear contraseña
    password = hash_passw(password)

    try:
        # Añadir la nueva cuenta a la DB
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s)', (username, password, email,))
        mysql.connection.commit()

    except Exception as e:
        response['ok'] = False
        response['error'] = str(e)

    finally:
        cursor.close()

    return response


@app.route('/get_public_routes', methods=['GET'])
def get_public_routes():

    # Inicializar el JSON de respuesta
    response = {'ok': True, 'data': None, 'error':''}
    
    try:
        # Consultar la DB para obtener las rutas publicas
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM rutas WHERE public = 1")
        public_routes = cursor.fetchall()

        # Añadir las rutas publicas en el JSON
        response['data'] = public_routes

    except Exception as e:
        response['ok'] = False
        response['error'] = str(e)

    finally:
        cursor.close()

    return response

@app.route('/get_user_info', methods=['GET'])
def get_user_info():

    # Inicializar el JSON de respuesta
    response = {'ok': True, 'error':''}

    # Recoger los datos de la peticion
    data = request.json
    username = data.get('username')

    try:
        # Extraer toda la informacion del usuario de la DB
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()

        # Si el usuario existe añadir la informacion de su cuenta en el JSON
        if account:
            response['data'] = account
    
    except Exception as e:
        response['ok'] = False
        response['error'] = str(e)

    finally:
        cursor.close()

    return response

@app.route('/get_route_info', methods=['GET'])
def get_route_info():

    # Inicializar el JSON de respuesta
    response = {'ok': True, 'error':''}

    # Recoger los datos de la peticion
    data = request.json
    route_id = data.get('route_id')

    try:
        # Extraer toda la informacion de la ruta de la DB
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM rutas WHERE id = %s', (route_id,))
        route = cursor.fetchone()

        # Si la ruta existe añadir toda su informacion en el JSON
        if route:
            response['data'] = route
    
    except Exception as e:
        response['ok'] = False
        response['error'] = str(e)

    finally:
        cursor.close()

    return response



@app.route('/get_user_routes', methods=['GET'])
def get_user_routes():

    # Inicializar el JSON de respuesta
    response = {'ok': True, 'error':''}
    
    # Recoger los datos de la peticion
    data = request.json
    email = data.get('email')
    
    try:
        # Consultar la DB para obtener las rutas del usuario
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM rutas WHERE email = %s", (email,))
        user_routes = cursor.fetchall()

        # Añadir todas las rutas del usuario en el JSON
        response['data'] = user_routes

    except Exception as e:
        response['ok'] = False
        response['error'] = str(e)

    finally:
        cursor.close()

    return response

@app.route('/delete_route', methods=['POST'])
def delete_route():

    # Inicializar el JSON de respuesta
    response = {'ok': True, 'error':''}
    
    # Recoger los datos de la peticion
    data = request.json
    route_id = data.get('route_id')

    try:
        # Eliminar la ruta de la DB
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("DELETE FROM rutas WHERE id = %s", (route_id,))
        mysql.connection.commit()

    except Exception as e:
        response['ok'] = False
        response['error'] = str(e)

    finally:
        cursor.close()
    
    return response

@app.route('/add_route', methods=['POST'])
def add_route():

    # Inicializar el JSON de respuesta
    response = {'ok': True, 'error':''}
    
    # Recoger los datos de la peticion
    data = request.json
    nombre = data.get('nombre')
    public = data.get('public')
    dificultad = data.get('dificultad')
    distancia = data.get('distancia')
    desnivel = data.get('desnivel')
    link = data.get('link')
    email = data.get('email')

    try:
        # Insertar los datos de la ruta en la DB
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'INSERT INTO rutas (nombre, public, dificultad, distancia, desnivel, link, email) VALUES (%s, %s, %s, %s, %s, %s, %s)',
            (nombre, public, dificultad, distancia, desnivel, link, email)
        )
        mysql.connection.commit()

    except Exception as e:
        response['ok'] = False
        response['error'] = str(e)
        
    finally:
        cursor.close()
    
    return response

@app.route('/update_route', methods=['POST'])
def update_route():

    # Inicializar el JSON de respuesta
    response = {'ok': True, 'error':''}

    # Recoger los datos de la peticion
    data = request.json
    route_id = data.get('route_id')
    nombre = data.get('nombre')
    dificultad = data.get('dificultad')
    distancia = data.get('distancia')
    desnivel = data.get('desnivel')
    link = data.get('link')
    public = data.get('public')

    try:
        # Actualizar la ruta en la DB con los datos nuevos
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""
            UPDATE rutas 
            SET nombre=%s, dificultad=%s, distancia=%s, desnivel=%s, link=%s, public=%s
            WHERE id=%s
        """, (nombre, dificultad, distancia, desnivel, link, public, route_id))
        mysql.connection.commit()

    except Exception as e:
        response['ok'] = False
        response['error'] = str(e)

    finally:
        cursor.close()

    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5003)
