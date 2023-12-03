# Sistema_Web_Docker

A continuación se proporcionan las instrucciones necesarias para desplegar la aplicación contenida en este repositorio haciendo uso de las herramientas _docker compose_ y _kubernetes_.

## PASO INICIAL: Clonado del repositorio

Ejecutar el siguiente comando en el directorio donde se desee clonar el repositorio:

```bash
git clone https://github.com/Sergiom8m/Sistema_Web_Docker
```

## OPCIÓN 1: Puesta en marcha empleando _docker compose_

Para desplegar la aplicación utilizando _docker_ se debe de tener instalada dicha aplicación con su correspondiente complemento, si fuese necesario para hacer uso de _docker compose_.

#### PASO 1: Adaptar los ficheros de configuración

Para que la aplicación funcione correctamente se deben editar varios ficheros de configuración.

1. En el fichero `/docker-compose.yml`:
    
    - Localizar el servicio 'app'
    - En el apartado 'labels', se debe modificar la segunda etiqueta: `traefik.http.routers.app.rule=Host(localhost)`. Donde indica `localhost` se debe poner la dirección IP del servidor donde se vaya a servir la aplicación. En caso de ejecutarlo de manera local no se debe modificar esta etiqueta.

2. En el directorio `/API-db`, en el fichero `config.py`:
    
    - La clave `MYSQL_PASSWORD` se puede modificar si se desea cambiar la clave del usuario `root` de la base de datos. La clave por defecto es `sysadminEHU`
    - En caso de cambiar la contraseña se debe modificar también la clave `MYSQL_ROOT_PASSWORD` en el servicio `db` del fichero `docker_compose.yml` 

3. En el directorio `/API-emails`, en el fichero `config.py`:

    - Las claves `GMAIL_USER` y `GMAIL_PASSWORD` deberían contener el email y la contraseña de aplicación del servicio de correo electrónico de la persona que gestiona la aplicación. 

    - Por defecto se ha establecido un usuario y una contraseña para que funcione sin necesidad de modificar nada.

Realizadas estas modificaciones en los archivos de configuración, la aplicación está lista para desplegarse.

#### PASO 2: Poner en marcha la aplicación

Para poner en marcha la aplicación, ejecutar el siguiente comando desde el directorio general del repositorio (contiene el fichero `docker-compose.yml`):

```bash
docker compose up -d
```

Tras una breve espera se observará que los contenedores están en marcha, entonces la aplicación estará en marcha y lista para ser usada.

#### PASO 3: Acceder a la aplicación desde el navegador

La aplicación está preparada para servirse en el puerto 80, por lo tanto, con acceder a la IP del servidor donde se ejecuta desde el navegador web sería suficiente para empezar a usar la aplicación. 

Si se está desplegando la aplicación en un entorno local con acceder a `localhost` sería suficiente.



## OPCIÓN 2: Puesta en marcha empleando _kubernetes_

La configuración contenida en este repositorio está dirigida a desplegarse con `Kubernetes Engine` de Google. Puede que el despliegue con otro motor de _kubernetes_ requiera de pequeñas modificaciones en la configuración.

#### PASO 1: Adaptar de los ficheros de configuración

En el despliegue con _kubernetes_ se usan las imágenes previamente creadas y alojadas en `DockerHub`:

\\[Imagen app](https://hub.docker.com/repository/docker/sergiom8m8/app/general) \\
[Imagen api-emails](https://hub.docker.com/repository/docker/sergiom8m8/api-emails/general) \\
[Imagen api-db](https://hub.docker.com/repository/docker/sergiom8m8/api-db/general) \\

Por ello, el despliegue con _kubernetes_ no acepta modificaciones en la configuración. Si se desease cambiar la configuración sería necesario modificar las imágenes.

#### PASO 2: Poner en marcha la aplicación:

Para desplegar la aplicación se debe ejecutar el siguiente comando desde el directorio `/k8s` del repositorio.

```bash
kubectl apply -f .
```

#### PASO 3: Acceder a la aplicación desde el navegador

Para acceder a la aplicación es suficiente con acceder desde el navegador a la IP del clúster de _kubernetes_ en la ruta `/` o cualquier otra que cuelgue de ese _path_.

Por ejemplo: \
\
`http://34.125.431.26/`

**Nota:** En _GKE_ puede tardar un tiempo bastante elevado que el objeto _ingress_ sea funcional. En caso de que la pagina web no se visualice reiniciar el despliegue ejecutando los siguientes comandos en el directorio `/k8s`:

```bash
kubectl delete -f .
```
```bash
kubectl apply -f .
```

[Bug GKE](https://stackoverflow.com/questions/51994508/gcp-load-balancer-backend-status-unknown)