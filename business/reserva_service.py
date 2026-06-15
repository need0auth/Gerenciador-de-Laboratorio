# business/reserva_service.py
from business.validation import (
    BusinessException,
    ReservationValidator,
    EntityExistenceStrategy,
    TimeConflictStrategy,
    UserPermissionStrategy
)

class ReservaService:
    def __init__(self, connection_manager, dao_factory):
        self.connection_manager = connection_manager
        self.dao_factory = dao_factory

    def solicitar_reserva(self, reserva):
        """
        Validates and saves a new reservation.
        Applies GoF Strategy Pattern validation logic.
        """
        if not reserva.laboratorio_id or not reserva.usuario_id or not reserva.data_inicio or not reserva.data_fim or not reserva.finalidade:
            raise BusinessException("Laboratório, Usuário, Data de início, Data de fim e Finalidade são obrigatórios.")
        
        # Set default status if not set
        if not reserva.status:
            reserva.status = 'PENDENTE'
            
        conn = self.connection_manager.get_connection()
        try:
            # Construct Validator and add validation strategies (GoF Strategy)
            validator = ReservationValidator()
            validator.add_strategy(EntityExistenceStrategy())
            validator.add_strategy(UserPermissionStrategy())
            validator.add_strategy(TimeConflictStrategy())
            
            # Execute validation strategies
            validator.validate(conn, self.dao_factory, reserva)
            
            reserva_dao = self.dao_factory.get_reserva_dao(conn)
            return reserva_dao.insert(reserva)
        finally:
            conn.close()

    def listar_reservas(self):
        conn = self.connection_manager.get_connection()
        try:
            reserva_dao = self.dao_factory.get_reserva_dao(conn)
            return reserva_dao.find_all()
        finally:
            conn.close()

    def buscar_reserva_por_id(self, id_reserva):
        conn = self.connection_manager.get_connection()
        try:
            reserva_dao = self.dao_factory.get_reserva_dao(conn)
            return reserva_dao.find_by_id(id_reserva)
        finally:
            conn.close()

    def atualizar_reserva(self, reserva):
        """
        Validates and updates an existing reservation.
        """
        if not reserva.id:
            raise BusinessException("ID da reserva é necessário para atualização.")
        if not reserva.laboratorio_id or not reserva.usuario_id or not reserva.data_inicio or not reserva.data_fim or not reserva.finalidade or not reserva.status:
            raise BusinessException("Todos os campos de reserva são obrigatórios para a atualização.")
            
        conn = self.connection_manager.get_connection()
        try:
            # Run validation strategies (GoF Strategy)
            validator = ReservationValidator()
            validator.add_strategy(EntityExistenceStrategy())
            validator.add_strategy(UserPermissionStrategy())
            validator.add_strategy(TimeConflictStrategy())
            
            validator.validate(conn, self.dao_factory, reserva)
            
            reserva_dao = self.dao_factory.get_reserva_dao(conn)
            reserva_dao.update(reserva)
        finally:
            conn.close()

    def remover_reserva(self, id_reserva):
        conn = self.connection_manager.get_connection()
        try:
            reserva_dao = self.dao_factory.get_reserva_dao(conn)
            existing = reserva_dao.find_by_id(id_reserva)
            if not existing:
                raise BusinessException(f"Reserva com ID {id_reserva} não encontrada.")
            reserva_dao.delete(id_reserva)
        finally:
            conn.close()

    def obter_usuario_relacionado(self, id_reserva):
        """
        Fetches the user details related to a specific reservation (related data query).
        """
        conn = self.connection_manager.get_connection()
        try:
            reserva_dao = self.dao_factory.get_reserva_dao(conn)
            existing = reserva_dao.find_by_id(id_reserva)
            if not existing:
                raise BusinessException(f"Reserva com ID {id_reserva} não encontrada.")
            return reserva_dao.get_related_usuario(id_reserva)
        finally:
            conn.close()

    def obter_laboratorio_relacionado(self, id_reserva):
        """
        Fetches the laboratory details related to a specific reservation (related data query).
        """
        conn = self.connection_manager.get_connection()
        try:
            reserva_dao = self.dao_factory.get_reserva_dao(conn)
            existing = reserva_dao.find_by_id(id_reserva)
            if not existing:
                raise BusinessException(f"Reserva com ID {id_reserva} não encontrada.")
            return reserva_dao.get_related_laboratorio(id_reserva)
        finally:
            conn.close()
