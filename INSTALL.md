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

$ pip install psycopg2

Luego deberá crear el usuario y la base de datos para la aplicación. Desde el
usuario postgres basta con ejecutar los siguientes comandos en el intérprete
del manejador:

sudo service postgresql start
sudo sudo -u postgres psql

```sql
CREATE USER synergy WITH PASSWORD 'lacontraseña';
CREATE DATABASE ci3715_db OWNER synergy;
```

Iniciar en Postgres en la base de datos creada
sudo sudo -u postgres psql -d ci3715_db

Puede cambiar estos valores, pero recuerde cambiarlos también en base.py

### 3. Crear una carpeta aplicaciones:

    mkdir aplicaciones

### 4. Crear el ambiente virtual

En una ventana de comandos cambiar a la carpeta principal de la aplicación.

    cd aplicaciones

Para crear el ambiente virtual:

    pyvenv-3.4 --without-pip --system-site-packages venv3

Si el comando anterior falla, intente con:

    python3 -m venv --without-pip --system-site-packages venv3

### 5. Descomprimir o copiar los archivos de esta distribución

Desde Github puede descargar el repositorio como zip. Si tiene instalado
[git](https://git-scm.com/) puede clonar el repositorio:

    git clone https://github.com/AlfJF/synergy_website.git

### 6. Activar el ambiente virtual

    source venv3/bin/activate

### 7. Instalar Flask

    pip3 install flask

(Puede que necesite ejecutarlo con sudo)

### 8. Instalar la gestión de opciones del servidor web

    pip3 install flask-script

(Puede que necesite ejecutarlo con sudo)

### 9. Ejecute la primera migración de la base de datos

    python base.py db init
    python base.py db migrate
    python base.py db upgrade

### 10. Ejecutar la aplicación

    python base.py runserver

El servidor quedará ejecutando indefinidamente.
Puede abrir en un navegador la dirección http://127.0.0.1:8080/
para entrar en la aplicación.

Para detener el servidor escriba Ctrl-c en la cónsola en la que se ejecuta.

Para instalar con Miniconda:
Crear ambiente:

    conda create -n condaenv3 python=3.4
    source activate condaenv3

Instalar paquetes

    conda install flask
    conda install --channel https://conda.anaconda.org/ziff flask-script
    conda install --channel https://conda.anaconda.org/hugo flask-sqlalchemy
(Flask-Migrate no está empaquetado para anaconda)
