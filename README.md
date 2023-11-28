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
    - En el apartado 'labels', se debe modificar la segunda etiqueta ('traefik.http.routers.app.rule=Host(`localhost`)')

### PASO 2: Situarse en el directorio general del repositorio (ubicación del archivo docker-compose.yaml)

### PASO 3: Poner en marcha la aplicación

### PASO 4: Acceder a la aplicación desde el navegador


## OPCION 2:Puesta en marcha empleando _kubernetes_