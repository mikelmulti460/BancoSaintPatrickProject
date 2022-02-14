## Bank Saint Patrick Project
**Instalación del API**
Usamos Docker para montar el servidor de desarrollo

 1. Configurar variables de entorno

 Se debe crear un archivo llamado "*.dev.env*" en la ruta principal del proyecto que contenga las siguientes variables

    DEBUG=1
	DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
	
configuración de la base de datos
	
	SQL_ENGINE=django.db.backends.postgresql_psycopg2
	SQL_DATABASE=bank
	SQL_USER=bank_admin
	SQL_HOST=db(No modificar)
	SQL_PORT=5432
	POSTGRES_PASSWORD=superpassword(contraseña del usuario root de postgres)
	SQL_PASSWORD=databasepass(contraseña de la {SQL_DATABASE})
	CF_INSTALACION=1
Configuración del super usuario
	
	SUPER_USER_MAIL=admin
	SUPER_USER_NAME=admin
	SUPER_USER_LASTNAME=admin
	SUPER_USER_PASSWORD=admin
	SECRET_KEY=LoremipsumdolorsitametconsecteturadipiscingelitEnteroac
Configuración de la clave de encriptación
	
	pip install cryptography
	home/project/> python3 
	>>> from cryptography.fernet import Fernet
	>>> # Put this somewhere safe!
	>>> key = Fernet.generate_key()
	LyqqYAuGJkWmzxwHl7qRqBHFkehiuAFODUfnM4zZYso=
	
	SECRET_KEY_DATA=LyqqYAuGJkWmzxwHl7qRqBHFkehiuAFODUfnM4zZYso=

 2. Activación del contenedor

    
    docker-compose up -d --build

	> El puerto predeterminado es 80
	> Puedes acceder mediante localhost:80
	> Si quieres cambiar de puerto, modifica el archivo "docker-compose.yml" 
	> En la parte de:
	> ports:
	> - 80:8000
	> cambia a :	 
	> - tupuerto:8000

   
   

