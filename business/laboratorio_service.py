# business/laboratorio_service.py
from business.validation import BusinessException

class LaboratorioService:
    def __init__(self, connection_manager, dao_factory):
        self.connection_manager = connection_manager
        self.dao_factory = dao_factory

    def cadastrar_laboratorio(self, laboratorio):
        if not laboratorio.nome or not laboratorio.sala or laboratorio.capacidade is None:
            raise BusinessException("Nome, sala e capacidade são obrigatórios.")
        if laboratorio.capacidade <= 0:
            raise BusinessException("A capacidade do laboratório deve ser maior que zero.")
            
        conn = self.connection_manager.get_connection()
        try:
            lab_dao = self.dao_factory.get_laboratorio_dao(conn)
            return lab_dao.insert(laboratorio)
        finally:
            conn.close()

    def listar_laboratorios(self):
        conn = self.connection_manager.get_connection()
        try:
            lab_dao = self.dao_factory.get_laboratorio_dao(conn)
            return lab_dao.find_all()
        finally:
            conn.close()

    def buscar_laboratorio_por_id(self, id_laboratorio):
        conn = self.connection_manager.get_connection()
        try:
            lab_dao = self.dao_factory.get_laboratorio_dao(conn)
            return lab_dao.find_by_id(id_laboratorio)
        finally:
            conn.close()

    def atualizar_laboratorio(self, laboratorio):
        if not laboratorio.id:
            raise BusinessException("ID do laboratório é necessário para atualização.")
        if not laboratorio.nome or not laboratorio.sala or laboratorio.capacidade is None:
            raise BusinessException("Nome, sala e capacidade não podem ser nulos ou vazios.")
        if laboratorio.capacidade <= 0:
            raise BusinessException("A capacidade do laboratório deve ser maior que zero.")

        conn = self.connection_manager.get_connection()
        try:
            lab_dao = self.dao_factory.get_laboratorio_dao(conn)
            lab_dao.update(laboratorio)
        finally:
            conn.close()

    def remover_laboratorio(self, id_laboratorio):
        conn = self.connection_manager.get_connection()
        try:
            lab_dao = self.dao_factory.get_laboratorio_dao(conn)
            existing = lab_dao.find_by_id(id_laboratorio)
            if not existing:
                raise BusinessException(f"Laboratório com ID {id_laboratorio} não encontrado.")
            lab_dao.delete(id_laboratorio)
        finally:
            conn.close()

    def listar_equipamentos_do_laboratorio(self, id_laboratorio):
        """
        Retrieves all equipment located in a specific laboratory.
        """
        conn = self.connection_manager.get_connection()
        try:
            lab_dao = self.dao_factory.get_laboratorio_dao(conn)
            existing = lab_dao.find_by_id(id_laboratorio)
            if not existing:
                raise BusinessException(f"Laboratório com ID {id_laboratorio} não encontrado.")
            return lab_dao.get_related_equipments(id_laboratorio)
        finally:
            conn.close()

    def listar_reservas_do_laboratorio(self, id_laboratorio):
        """
        Retrieves all reservations for a specific laboratory.
        """
        conn = self.connection_manager.get_connection()
        try:
            lab_dao = self.dao_factory.get_laboratorio_dao(conn)
            existing = lab_dao.find_by_id(id_laboratorio)
            if not existing:
                raise BusinessException(f"Laboratório com ID {id_laboratorio} não encontrado.")
            return lab_dao.get_related_reservations(id_laboratorio)
        finally:
            conn.close()
