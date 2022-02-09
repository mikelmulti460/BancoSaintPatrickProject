import psycopg2
import os
dbpass = os.environ.get('SQL_PASSWORD','postgress')
dbname = os.environ.get('SQL_DATABASE','postgress')
dbuser = os.environ.get('SQL_USER','postgress')
pg_pass = os.environ.get('POSTGRES_PASSWORD','postgress')
#establishing the connection

conn = psycopg2.connect(
   database="postgres", user='postgres', password=f"{pg_pass}", host='db', port= '5432'
)
conn.autocommit = True

#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Preparing query to create a database
sql = [f"CREATE DATABASE {dbname};",
        f"CREATE USER {dbuser} WITH PASSWORD '{dbpass}'",
        f"ALTER ROLE {dbuser} SET client_encoding TO 'utf8';",
        f"ALTER ROLE {dbuser} SET default_transaction_isolation TO 'read committed';",
        f"ALTER ROLE {dbuser} SET timezone TO 'UTC';",
        f"GRANT ALL PRIVILEGES ON DATABASE {dbname} TO {dbuser};"]

#Creating a database
i=0
for sql in sql:
    i=i+1
    try:
        cursor.execute(sql)
        print(f"operation {i} successfully........")
    except (psycopg2.errors.DuplicateDatabase,psycopg2.errors.DuplicateObject):
        pass