# controllers/equipamento_controller.py
from models.equipamento import Equipamento
from business.validation import BusinessException

class EquipamentoController:
    def __init__(self, equipamento_service):
        self.equipamento_service = equipamento_service

    def cadastrar(self, nome, marca, num_serie, laboratorio_id, status):
        """
        Action to register a new equipment.
        """
        try:
            equipamento = Equipamento(nome=nome, marca=marca, num_serie=num_serie, laboratorio_id=laboratorio_id, status=status)
            eq_salvo = self.equipamento_service.cadastrar_equipamento(equipamento)
            return {
                "success": True,
                "message": "Equipamento cadastrado com sucesso!",
                "data": eq_salvo.to_dict()
            }
        except BusinessException as e:
            return {"success": False, "message": e.message}
        except Exception as e:
            return {"success": False, "message": f"Erro inesperado: {str(e)}"}

    def listar(self):
        """
        Action to list all equipment.
        """
        try:
            equipamentos = self.equipamento_service.listar_equipamentos()
            return {
                "success": True,
                "data": [eq.to_dict() for eq in equipamentos]
            }
        except Exception as e:
            return {"success": False, "message": f"Erro ao listar equipamentos: {str(e)}"}

    def buscar_por_id(self, id_equipamento):
        """
        Action to retrieve an equipment by ID.
        """
        try:
            eq = self.equipamento_service.buscar_equipamento_por_id(id_equipamento)
            if eq:
                return {
                    "success": True,
                    "data": eq.to_dict()
                }
            return {"success": False, "message": f"Equipamento com ID {id_equipamento} não encontrado."}
        except Exception as e:
            return {"success": False, "message": f"Erro ao buscar equipamento: {str(e)}"}

    def atualizar(self, id_equipamento, nome, marca, num_serie, laboratorio_id, status):
        """
        Action to update an equipment.
        """
        try:
            equipamento = Equipamento(id_equipamento=id_equipamento, nome=nome, marca=marca, num_serie=num_serie, laboratorio_id=laboratorio_id, status=status)
            self.equipamento_service.atualizar_equipamento(equipamento)
            return {
                "success": True,
                "message": "Equipamento atualizado com sucesso!"
            }
        except BusinessException as e:
            return {"success": False, "message": e.message}
        except Exception as e:
            return {"success": False, "message": f"Erro inesperado ao atualizar: {str(e)}"}

    def remover(self, id_equipamento):
        """
        Action to delete an equipment.
        """
        try:
            self.equipamento_service.remover_equipamento(id_equipamento)
            return {
                "success": True,
                "message": "Equipamento removido com sucesso!"
            }
        except BusinessException as e:
            return {"success": False, "message": e.message}
        except Exception as e:
            return {"success": False, "message": f"Erro inesperado ao remover: {str(e)}"}
