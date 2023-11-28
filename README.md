# Sistema_Web_Docker

A continuación se proporcionan las instrucciones necesarias para desplegar la aplicación contenida en este repositorio haciendo uso de las herramientas _docker Compose_ y _kubernetes_.

## PASO INCIAL: Clonado del repositorio

Ejecutar el siguiente comando en el directorio donde se desee clonar el repositorio:

```bash
git clone https://github.com/Sergiom8m/Sistema_Web_Docker
```

## OPCION 1: Puesta en marcha empleando _docker compose_

Para desplegar la aplicación utilizando _docker_ se debe de tener instalada dicha aplicación con su correspondiente complemento si fuese necesario para hacer uso se _docker compose_.

### PASO 1: Adaptar los ficheros de configuración

Para que la aplicacion funcione correctamente se deben editar varios ficheros de configuración.

1. En el fichero 'docker-compose.yml':
    
    - Localizar el servicio 'app'
    - En el apartado 'labels', se debe modificar la segunda etiqueta: `traefik.http.routers.app.rule=Host(localhost)`. Donde indica `localhost` se debe poner la dirección IP del sevidor donde se vaya a servir la aplicacion. En caso de ejecutarlo de manera local no se debe modificar esta etiqueta.

2. En el directorio `API-db`, en el fichero `config.py`:
    
    - La clave `MYSQL_PASSWORD` se puede modificar si se desea cambiar la clave del usuario `root` de la base de datos. La clave por defecto es `sysadminEHU`
    - En caso de cambiar la contraseña se debe modificar tambien la clave `MYSQL_ROOT_PASSWORD` en el servicio `db` del fichero `docker_compose.yml` 

3. En el directorio `API-emails`, en el fichero `config.py`:

    - Las claves `GMAIL_USER` y `GMAIL_PASSWORD` deberian contener el email y la contraseña de aplicacion del servicio de correo electronico de la persona que gestiona la aplicacion. 

Realizadas estas modificaciones en los archivos de configuración la aplicacion esta lista para desplegarse.

### PASO 2: Poner en marcha la aplicación

Para poner en marcha la aplicacion ejecutar el siguiente comando desde el directorio general del repositorio (contiene el fichero `docker-compose.yml`):

```bash
docker compose up -d
```

Tras una breve espera se observará que los contenedores estan en marcha, entonces la aplicacion estara en marcha y lista para ser usada.

### PASO 3: Acceder a la aplicación desde el navegador

La aplicacion esta preparada para servirse en el puerto 80, por lo tanto con acceder a la IP del servidor donde se ejecuta desde el navegador web seria suficiente para empezar a usar la aplicacion. 

Si se esta desplegando la aplicacion en un entorno local con acceder a `localhost` seria suficiente.



## OPCION 2: Puesta en marcha empleando _kubernetes_

La configuracion contenida en este repositorio esta dirigida a desplegarse con `Kubernetes Engine` de Google. Puede que el despliegue con otro motor de _kubernetes_ requiera de pequeñas modificaciones en la configuracion.

### PASO 1: Adaptar de los ficheros de configuracion

En el despliegue con _kubernetes_ se usan las imagenes previamente creadas y alojadas en `DockerHub`:

[https://hub.docker.com/repository/docker/sergiom8m8/app/general](imagen app)
[https://hub.docker.com/repository/docker/sergiom8m8/api-emails/general](api emails)
[https://hub.docker.com/repository/docker/sergiom8m8/api-db/general](api db)

Por ello, el despliegue con _kubernetes_ no acepta modificaciones en la configuracion. Si se desease cambiar la configuracion seria necesario modificar las imagenes.

### PASO 2: Poner en marcha la aplicacion:

Para desplegar la aplicacion se debe ejecutar el siguiente comando desde el directorio `k8s` del repositorio.

```bash
kubectl -f apply .
```

