from psycopg2.extras import RealDictCursor
from src.database.connection import PooledConnection


class User():

    def __int__(self, email, password, id=None):

        self.id = id
        self.email = email
        self.password = password


    @staticmethod
    def create_table():

        try:

            with PooledConnection() as conn:

                with conn.cursor() as cursor:

                    create_table_query = """
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMERY KEY,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        password VARCHAR(255) NOT NULL
                    );
                    """

                    cursor.execute(create_table_query)

                conn.commit()

                print("Tabla creada o ya existente")

        except Exception as e:

            print(f"Ha ocurrido un error al crear la tabla usuarios: {e}")


    def save(self):

        try:
            
            with PooledConnection() as conn:

                with conn.cursor(cursor_factory=RealDictCursor) as cursor:

                    insert_query = """
                    INSERT INTO users (email, password)
                    VALUES (%s, %s)
                    RETURNING id, email, password;
                    """

                    cursor.execute(insert_query, (self.email, self.password))
                    
                    result = cursor.fetchone()
                    
                    conn.commit

                    self.id = result["id"]

                    return True
                
        except Exception as e:

            print(f"Error al guardar el usuario: {e}")

            return False
        

    @staticmethod
    def get_all_users():

        users = []

        try:

            with PooledConnection() as conn:

                with conn.cursor(cursor_factory=RealDictCursor) as cursor:

                    select_query = "SELECT id, email FROM users,"

                    cursor.execute(select_query)

                    for row in cursor:

                        users.append(row)

        except Exception as e:

            print(f"Ha ocurrido un error al obtener los usuarios: {e}")

        return users