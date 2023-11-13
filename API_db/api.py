from flask import Flask, render_template, redirect, url_for, request
from config import SECRET_APP_KEY, MYSQL_PASSWORD
from flask_mysqldb import MySQL
import MySQLdb.cursors
import MySQLdb.cursors
import hashlib

app = Flask(__name__)

app.secret_key = SECRET_APP_KEY

app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = MYSQL_PASSWORD
app.config['MYSQL_DB'] = 'appDb'

mysql = MySQL(app)

def hash_passw(password):
    hash = password + app.secret_key
    hash = hashlib.sha1(hash.encode())
    password = hash.hexdigest()
    return password


@app.route('/check_user_psswd', methods=['POST'])
def check_user_psswd():

    response = {'ok': False, 'data':None, 'error':''}

    # Recoger los datos de la peticion
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Hashear contraseña
    password = hash_passw(password)

    try:
    # Comprobar si la cuenta existe en la base de datos
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password,))
        account = cursor.fetchone()

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

    response = {'ok': True, 'error': ''}

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

    response = {'ok': True, 'data': None}
    
    try:
        # Consultar la base de datos para obtener las rutas publicas
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM rutas WHERE public = 1")
        public_routes = cursor.fetchall()

        response['data'] = public_routes

    except:
        response['ok'] = False

    finally:
        cursor.close()

    return response

@app.route('/get_user_info', methods=['GET'])
def get_user_info():

    response = {'ok': True}

    data = request.json
    username = data.get('username')

    try:
        # Extraer toda la informacion del usuario de la DB
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()

        if account:
            response['data'] = account
    
    except:
        response = {'ok': False}

    finally:
        cursor.close()

    return response

@app.route('/get_route_info', methods=['GET'])
def get_route_info():

    response = {'ok': True}

    data = request.json
    route_id = data.get('route_id')

    try:
        # Extraer toda la informacion del usuario de la DB
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM rutas WHERE id = %s', (route_id,))
        route = cursor.fetchone()

        if route:
            response['data'] = route
    
    except:
        response = {'ok': False}

    finally:
        cursor.close()

    return response



@app.route('/get_user_routes', methods=['GET'])
def get_user_routes():

    response = {'ok': True}
    
    # Recoger los datos de la peticion
    data = request.json
    email = data.get('email')
    
    try:
        # Consultar la base de datos para obtener las rutas del usuario
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM rutas WHERE email = %s", (email,))
        user_routes = cursor.fetchall()

        response['data'] = user_routes

    except:
        response['ok'] = False

    finally:
        cursor.close()

    return response

@app.route('/delete_route', methods=['POST'])
def delete_route():

    response = {'ok': True}
    
    # Recoger los datos de la peticion
    data = request.json
    route_id = data.get('route_id')

    try:
        # Eliminar la ruta de la DB
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("DELETE FROM rutas WHERE id = %s", (route_id,))
        mysql.connection.commit()

    except:
        response = {'ok': False}

    finally:
        cursor.close()
    
    return response

@app.route('/add_route', methods=['POST'])
def add_route():

    response = {'ok': True}
    
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
        # Inserta los datos en la base de datos
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'INSERT INTO rutas (nombre, public, dificultad, distancia, desnivel, link, email) VALUES (%s, %s, %s, %s, %s, %s, %s)',
            (nombre, public, dificultad, distancia, desnivel, link, email)
        )
        mysql.connection.commit()

    except:
         response = {'ok': False}
        
    finally:
        cursor.close()
    
    return response

@app.route('/update_route', methods=['POST'])
def update_route():
    response = {'ok': False, 'error': ''}

    data = request.json
    route_id = data.get('route_id')
    nombre = data.get('nombre')
    dificultad = data.get('dificultad')
    distancia = data.get('distancia')
    desnivel = data.get('desnivel')
    link = data.get('link')
    public = data.get('public')

    try:
        # Actualizar la ruta en la base de datos
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""
            UPDATE rutas 
            SET nombre=%s, dificultad=%s, distancia=%s, desnivel=%s, link=%s, public=%s
            WHERE id=%s
        """, (nombre, dificultad, distancia, desnivel, link, public, route_id))
        mysql.connection.commit()

        response['ok'] = True

    except Exception as e:
        response['error'] = str(e)

    finally:
        cursor.close()

    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5003)
