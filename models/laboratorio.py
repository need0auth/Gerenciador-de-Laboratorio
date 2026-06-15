# models/laboratorio.py

class Laboratorio:
    def __init__(self, id_laboratorio=None, nome=None, sala=None, capacidade=None, descricao=None):
        self.id = id_laboratorio
        self.nome = nome
        self.sala = sala
        self.capacidade = capacidade
        self.descricao = descricao

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "sala": self.sala,
            "capacidade": self.capacidade,
            "descricao": self.descricao
        }
