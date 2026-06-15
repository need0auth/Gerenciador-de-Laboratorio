# models/equipamento.py

class Equipamento:
    def __init__(self, id_equipamento=None, nome=None, marca=None, num_serie=None, laboratorio_id=None, status=None):
        self.id = id_equipamento
        self.nome = nome
        self.marca = marca
        self.num_serie = num_serie
        self.laboratorio_id = laboratorio_id
        self.status = status  # 'ATIVO', 'MANUTENCAO', 'INATIVO'

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "marca": self.marca,
            "num_serie": self.num_serie,
            "laboratorio_id": self.laboratorio_id,
            "status": self.status
        }
