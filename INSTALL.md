# Instrucciones para ejecutar esta aplicación bajo Linux
(para otros sistemas , por favor consultar la documentación de Flask)

### 1. Necesitará tener instalado pip3
Si no lo tiene instalado, puede hacerlo ejecutando el comando

    sudo apt-get install python3-pip

### 2. Prepare la base de datos

La aplicación utiliza PostgreSQL. Puede conseguir las instrucciones de
instalación [aquí](http://www.postgresql.org/download/).

También necesitará SQLAlchemy, que puede instalar con los siguientes comandos:

    sudo pip3 install SQLAlchemy
    sudo pip3 install Flask-SQLAlchemy
    sudo pip3 install Flask-Migrate

Para poder trabajar con PostgreSQL usando SQLAlchemy necesitará instalar
[psycopg2](http://initd.org/psycopg/docs/install.html).

Luego deberá crear el usuario y la base de datos para la aplicación:

```sql
CREATE USER synergy WITH PASSWORD 'lacontraseña';
CREATE DATABASE base_ci3725 OWNER synergy;
```

### 3. Crear una carpeta aplicaciones:

    mkdir aplicaciones

### 4. Crear el ambiente virtual

En una ventana de comandos cambiar a la carpeta principal de la aplicación.

    cd aplicaciones

Para crear el ambiente virtual

    pyvenv-3.4 --without-pip --system-site-packages venv3

### 5. Descomprimir o copiar los archivos de esta distribución

### 6. Activar el ambiente virtual

    source venv3/bin/activate

### 7. Instalar Flask
La primera vez que lo haga puede que necesite ejecutarlo con sudo.

    pip3 install flask

### 8. Instalar la gestión de opciones del servidor web
La primera vez que lo haga puede que necesite ejecutarlo con sudo.

    sudo pip3 install flask-script

### 9. Ejecutar la aplicación

    python base.py runserver

El servidor quedará ejecutando indefinidamente.
Puede abrir en un navegador la dirección
 http://127.0.0.1:5000/ para entrar en la aplicación.


Para detener el servidor
escribir Ctrl-c en la cónsola en la que ejecuta el servidor.

Cuando la aplicación ya está instalada y se quiere descargar de cohesión una nueva versión puede hacerlo con los pasos siguientes.

- Respaldar la versión anterior

    tar czvf ../SocialFl\`date +%y%m%d%H%M%S`.tgz {static,base.py,app,README.txt}

- Borrar la versión ya respaldada

    rm -rf {static,base.py,app,README.txt}

Descargar una nueva versión desde cohesión y
desempaquetarla en la carpeta de la aplicación:

    unzip socialFL.zip

Para instalar con Miniconda:
Crear ambiente:

    conda create -n condaenv3 python=3.4
    source activate condaenv3

Instalar paquetes

    conda install flask
    conda install --channel https://conda.anaconda.org/ziff flask-script
    conda install --channel https://conda.anaconda.org/hugo flask-sqlalchemy
(Flask-Migrate no está empaquetado para anaconda)
