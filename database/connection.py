# database/connection.py
import psycopg2

class ConnectionManager:
    def __init__(self, host="127.0.0.1", port=5432, database="gestao_laboratorio", user="lab_user", password="lab_password"):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password

    def get_connection(self):
        """
        Creates and returns a new PostgreSQL database connection.
        """
        return psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password
        )
