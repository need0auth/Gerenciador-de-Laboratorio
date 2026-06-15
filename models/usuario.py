# models/usuario.py

class Usuario:
    def __init__(self, id_usuario=None, nome=None, email=None, senha=None, tipo=None):
        self.id = id_usuario
        self.nome = nome
        self.email = email
        self.senha = senha
        self.tipo = tipo  # 'ALUNO', 'PROFESSOR', 'ADMINISTRADOR'

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "tipo": self.tipo
        }
