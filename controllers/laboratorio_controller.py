# controllers/laboratorio_controller.py
from models.laboratorio import Laboratorio
from business.validation import BusinessException

class LaboratorioController:
    def __init__(self, laboratorio_service):
        self.laboratorio_service = laboratorio_service

    def cadastrar(self, nome, sala, capacidade, descricao):
        """
        Action to register a new laboratory.
        """
        try:
            laboratorio = Laboratorio(nome=nome, sala=sala, capacidade=capacidade, descricao=descricao)
            lab_salvo = self.laboratorio_service.cadastrar_laboratorio(laboratorio)
            return {
                "success": True,
                "message": "Laboratório cadastrado com sucesso!",
                "data": lab_salvo.to_dict()
            }
        except BusinessException as e:
            return {"success": False, "message": e.message}
        except Exception as e:
            return {"success": False, "message": f"Erro inesperado: {str(e)}"}

    def listar(self):
        """
        Action to retrieve all laboratories.
        """
        try:
            labs = self.laboratorio_service.listar_laboratorios()
            return {
                "success": True,
                "data": [l.to_dict() for l in labs]
            }
        except Exception as e:
            return {"success": False, "message": f"Erro ao listar laboratórios: {str(e)}"}

    def buscar_por_id(self, id_laboratorio):
        """
        Action to find a laboratory by ID.
        """
        try:
            lab = self.laboratorio_service.buscar_laboratorio_por_id(id_laboratorio)
            if lab:
                return {
                    "success": True,
                    "data": lab.to_dict()
                }
            return {"success": False, "message": f"Laboratório com ID {id_laboratorio} não encontrado."}
        except Exception as e:
            return {"success": False, "message": f"Erro ao buscar laboratório: {str(e)}"}

    def atualizar(self, id_laboratorio, nome, sala, capacidade, descricao):
        """
        Action to update a laboratory.
        """
        try:
            laboratorio = Laboratorio(id_laboratorio=id_laboratorio, nome=nome, sala=sala, capacidade=capacidade, descricao=descricao)
            self.laboratorio_service.atualizar_laboratorio(laboratorio)
            return {
                "success": True,
                "message": "Laboratório atualizado com sucesso!"
            }
        except BusinessException as e:
            return {"success": False, "message": e.message}
        except Exception as e:
            return {"success": False, "message": f"Erro inesperado ao atualizar: {str(e)}"}

    def remover(self, id_laboratorio):
        """
        Action to delete a laboratory.
        """
        try:
            self.laboratorio_service.remover_laboratorio(id_laboratorio)
            return {
                "success": True,
                "message": "Laboratório removido com sucesso!"
            }
        except BusinessException as e:
            return {"success": False, "message": e.message}
        except Exception as e:
            return {"success": False, "message": f"Erro inesperado ao remover: {str(e)}"}

    def listar_equipamentos(self, id_laboratorio):
        """
        Action to retrieve all equipment associated with a specific laboratory (related query).
        """
        try:
            equipamentos = self.laboratorio_service.listar_equipamentos_do_laboratorio(id_laboratorio)
            return {
                "success": True,
                "data": [eq.to_dict() for eq in equipamentos]
            }
        except BusinessException as e:
            return {"success": False, "message": e.message}
        except Exception as e:
            return {"success": False, "message": f"Erro ao listar equipamentos do laboratório: {str(e)}"}

    def listar_reservas(self, id_laboratorio):
        """
        Action to retrieve all reservations for a specific laboratory (related query).
        """
        try:
            reservas = self.laboratorio_service.listar_reservas_do_laboratorio(id_laboratorio)
            return {
                "success": True,
                "data": [res.to_dict() for res in reservas]
            }
        except BusinessException as e:
            return {"success": False, "message": e.message}
        except Exception as e:
            return {"success": False, "message": f"Erro ao listar reservas do laboratório: {str(e)}"}
