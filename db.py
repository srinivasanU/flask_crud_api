import psycopg2

host = 'localhost'
database = 'contact_db'
user = 'contact_db_user'
password = 'contact_db_pwd'

def dbconnection():
    conn = psycopg2.connect(host=host, database=database, user=user, password=password)
    return conn