# models/reserva.py

class Reserva:
    def __init__(self, id_reserva=None, laboratorio_id=None, usuario_id=None, data_inicio=None, data_fim=None, finalidade=None, status=None):
        self.id = id_reserva
        self.laboratorio_id = laboratorio_id
        self.usuario_id = usuario_id
        self.data_inicio = data_inicio  # datetime object or string
        self.data_fim = data_fim      # datetime object or string
        self.finalidade = finalidade
        self.status = status  # 'PENDENTE', 'APROVADA', 'CANCELADA'

    def to_dict(self):
        return {
            "id": self.id,
            "laboratorio_id": self.laboratorio_id,
            "usuario_id": self.usuario_id,
            "data_inicio": str(self.data_inicio),
            "data_fim": str(self.data_fim),
            "finalidade": self.finalidade,
            "status": self.status
        }
