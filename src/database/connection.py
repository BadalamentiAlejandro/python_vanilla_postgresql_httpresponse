import os
import psycopg2
from psycopg2 import pool
from src.config.settings import DB_URL

# Se crea una clase para hacer un pool de conexiones que se utilizará en el resto de módulos.
# De esta manera se centraliza la conexión a la base de datos y solo se llama a la clase.

connection_pool = pool.ThreadedConnectionPool(minconn=1, maxconn=10, dsn=DB_URL)


class PooledConnection:

    def __init__(self):
        
        self.conn = None


    def __enter__(self):

        self.conn = connection_pool.getconn()

        return self.conn
    

    def __exit__(self, exc_type, exc_val, exc_tb):

        connection_pool.putconn(self.conn)

        return False