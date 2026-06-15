# dao/base_dao.py

class BaseDAO:
    def __init__(self, connection):
        if connection is None:
            raise ValueError("Conexão com o banco de dados não pode ser Nula.")
        self.connection = connection
