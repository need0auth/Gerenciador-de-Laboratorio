# dao/usuario_dao.py
from dao.base_dao import BaseDAO
from models.usuario import Usuario

class UsuarioDAO(BaseDAO):
    def insert(self, usuario):
        """
        Inserts a new user into the database and sets the generated ID.
        """
        sql = "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (%s, %s, %s, %s) RETURNING id;"
        with self.connection.cursor() as cur:
            cur.execute(sql, (usuario.nome, usuario.email, usuario.senha, usuario.tipo))
            usuario.id = cur.fetchone()[0]
        self.connection.commit()
        return usuario

    def find_by_id(self, id_usuario):
        """
        Finds a user by ID. Returns a Usuario instance or None.
        """
        sql = "SELECT id, nome, email, senha, tipo FROM usuarios WHERE id = %s;"
        with self.connection.cursor() as cur:
            cur.execute(sql, (id_usuario,))
            row = cur.fetchone()
            if row:
                return Usuario(id_usuario=row[0], nome=row[1], email=row[2], senha=row[3], tipo=row[4])
        return None

    def find_all(self):
        """
        Returns all users.
        """
        sql = "SELECT id, nome, email, senha, tipo FROM usuarios ORDER BY nome;"
        usuarios = []
        with self.connection.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
            for row in rows:
                usuarios.append(Usuario(id_usuario=row[0], nome=row[1], email=row[2], senha=row[3], tipo=row[4]))
        return usuarios

    def update(self, usuario):
        """
        Updates an existing user.
        """
        sql = "UPDATE usuarios SET nome = %s, email = %s, senha = %s, tipo = %s WHERE id = %s;"
        with self.connection.cursor() as cur:
            cur.execute(sql, (usuario.nome, usuario.email, usuario.senha, usuario.tipo, usuario.id))
        self.connection.commit()

    def delete(self, id_usuario):
        """
        Deletes a user by ID.
        """
        sql = "DELETE FROM usuarios WHERE id = %s;"
        with self.connection.cursor() as cur:
            cur.execute(sql, (id_usuario,))
        self.connection.commit()

    def find_by_email(self, email):
        """
        Finds a user by Email. Returns a Usuario instance or None.
        """
        sql = "SELECT id, nome, email, senha, tipo FROM usuarios WHERE email = %s;"
        with self.connection.cursor() as cur:
            cur.execute(sql, (email,))
            row = cur.fetchone()
            if row:
                return Usuario(id_usuario=row[0], nome=row[1], email=row[2], senha=row[3], tipo=row[4])
        return None
