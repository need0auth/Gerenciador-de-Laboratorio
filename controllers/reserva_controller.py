# controllers/reserva_controller.py
from models.reserva import Reserva
from business.validation import BusinessException

class ReservaController:
    def __init__(self, reserva_service):
        self.reserva_service = reserva_service

    def solicitar(self, laboratorio_id, usuario_id, data_inicio, data_fim, finalidade):
        """
        Action to request a new reservation.
        """
        try:
            reserva = Reserva(laboratorio_id=laboratorio_id, usuario_id=usuario_id, data_inicio=data_inicio, data_fim=data_fim, finalidade=finalidade)
            res_salva = self.reserva_service.solicitar_reserva(reserva)
            return {
                "success": True,
                "message": "Reserva solicitada com sucesso!",
                "data": res_salva.to_dict()
            }
        except BusinessException as e:
            return {"success": False, "message": e.message}
        except Exception as e:
            return {"success": False, "message": f"Erro inesperado: {str(e)}"}

    def listar(self):
        """
        Action to list all reservations.
        """
        try:
            reservas = self.reserva_service.listar_reservas()
            return {
                "success": True,
                "data": [r.to_dict() for r in reservas]
            }
        except Exception as e:
            return {"success": False, "message": f"Erro ao listar reservas: {str(e)}"}

    def buscar_por_id(self, id_reserva):
        """
        Action to retrieve a reservation by ID.
        """
        try:
            res = self.reserva_service.buscar_reserva_por_id(id_reserva)
            if res:
                return {
                    "success": True,
                    "data": res.to_dict()
                }
            return {"success": False, "message": f"Reserva com ID {id_reserva} não encontrada."}
        except Exception as e:
            return {"success": False, "message": f"Erro ao buscar reserva: {str(e)}"}

    def atualizar(self, id_reserva, laboratorio_id, usuario_id, data_inicio, data_fim, finalidade, status):
        """
        Action to update an existing reservation.
        """
        try:
            reserva = Reserva(
                id_reserva=id_reserva,
                laboratorio_id=laboratorio_id,
                usuario_id=usuario_id,
                data_inicio=data_inicio,
                data_fim=data_fim,
                finalidade=finalidade,
                status=status
            )
            self.reserva_service.atualizar_reserva(reserva)
            return {
                "success": True,
                "message": "Reserva atualizada com sucesso!"
            }
        except BusinessException as e:
            return {"success": False, "message": e.message}
        except Exception as e:
            return {"success": False, "message": f"Erro inesperado ao atualizar: {str(e)}"}

    def remover(self, id_reserva):
        """
        Action to delete a reservation.
        """
        try:
            self.reserva_service.remover_reserva(id_reserva)
            return {
                "success": True,
                "message": "Reserva removida com sucesso!"
            }
        except BusinessException as e:
            return {"success": False, "message": e.message}
        except Exception as e:
            return {"success": False, "message": f"Erro inesperado ao remover: {str(e)}"}

    def obter_usuario_relacionado(self, id_reserva):
        """
        Action to get the user associated with a reservation (related query).
        """
        try:
            usuario = self.reserva_service.obter_usuario_relacionado(id_reserva)
            if usuario:
                return {
                    "success": True,
                    "data": usuario.to_dict()
                }
            return {"success": False, "message": "Nenhum usuário associado a esta reserva."}
        except BusinessException as e:
            return {"success": False, "message": e.message}
        except Exception as e:
            return {"success": False, "message": f"Erro inesperado: {str(e)}"}

    def obter_laboratorio_relacionado(self, id_reserva):
        """
        Action to get the laboratory associated with a reservation (related query).
        """
        try:
            lab = self.reserva_service.obter_laboratorio_relacionado(id_reserva)
            if lab:
                return {
                    "success": True,
                    "data": lab.to_dict()
                }
            return {"success": False, "message": "Nenhum laboratório associado a esta reserva."}
        except BusinessException as e:
            return {"success": False, "message": e.message}
        except Exception as e:
            return {"success": False, "message": f"Erro inesperado: {str(e)}"}
