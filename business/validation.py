# business/validation.py
from datetime import datetime
from dao.factory import DAOFactory

class BusinessException(Exception):
    """Exception raised for errors in the business layer."""
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class ValidationStrategy:
    """
    Abstract Base Class representing a Validation Strategy.
    (GoF Strategy Pattern - Strategy Interface)
    """
    def __init__(self):
        pass

    def validate(self, connection, dao_factory, reserva):
        """
        Validates the reservation based on specific business rules.
        Should raise BusinessException if validation fails.
        """
        raise NotImplementedError("As estratégias concretas devem implementar o método 'validate'.")


class EntityExistenceStrategy(ValidationStrategy):
    """
    Strategy to verify if the referenced User and Laboratory actually exist.
    """
    def validate(self, connection, dao_factory, reserva):
        user_dao = dao_factory.get_usuario_dao(connection)
        lab_dao = dao_factory.get_laboratorio_dao(connection)

        usuario = user_dao.find_by_id(reserva.usuario_id)
        if not usuario:
            raise BusinessException(f"Usuário com ID {reserva.usuario_id} não existe no sistema.")

        laboratorio = lab_dao.find_by_id(reserva.laboratorio_id)
        if not laboratorio:
            raise BusinessException(f"Laboratório com ID {reserva.laboratorio_id} não existe no sistema.")


class TimeConflictStrategy(ValidationStrategy):
    """
    Strategy to verify if there are any conflicting (overlapping) approved reservations
    for the same laboratory in the specified timeframe.
    """
    def validate(self, connection, dao_factory, reserva):
        reserva_dao = dao_factory.get_reserva_dao(connection)
        
        # Check overlaps
        conflicts = reserva_dao.find_conflicting_reservations(
            reserva.laboratorio_id,
            reserva.data_inicio,
            reserva.data_fim,
            exclude_id=reserva.id
        )
        if conflicts:
            conflicting_info = f"ID: {conflicts[0].id} (de {conflicts[0].data_inicio} até {conflicts[0].data_fim})"
            raise BusinessException(
                f"Conflito de reserva detectado. O laboratório já está reservado nesse período pela Reserva {conflicting_info}."
            )


class UserPermissionStrategy(ValidationStrategy):
    """
    Strategy to verify user-specific permission rules:
    - ALUNO users can reserve a laboratory for a maximum of 4 hours.
    - PROFESSOR and ADMINISTRADOR have no time restriction.
    """
    def validate(self, connection, dao_factory, reserva):
        user_dao = dao_factory.get_usuario_dao(connection)
        usuario = user_dao.find_by_id(reserva.usuario_id)
        
        if not usuario:
            return  # Will be caught by EntityExistenceStrategy

        if usuario.tipo == "ALUNO":
            # Parse dates if they are strings, otherwise check difference directly
            start = reserva.data_inicio
            end = reserva.data_fim
            
            if isinstance(start, str):
                start = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
            if isinstance(end, str):
                end = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
                
            duration = end - start
            max_duration_seconds = 4 * 3600  # 4 hours
            
            if duration.total_seconds() > max_duration_seconds:
                raise BusinessException(
                    f"Usuários do tipo ALUNO ({usuario.nome}) não podem realizar reservas com duração superior a 4 horas. Duração solicitada: {duration.total_seconds() / 3600:.2f} horas."
                )


class ReservationValidator:
    """
    Context class that executes the validation strategies.
    (GoF Strategy Pattern - Context)
    """
    def __init__(self, strategies=None):
        if strategies is None:
            self.strategies = []
        else:
            self.strategies = strategies

    def add_strategy(self, strategy):
        self.strategies.append(strategy)

    def validate(self, connection, dao_factory, reserva):
        """
        Runs all registered validation strategies on the reservation.
        """
        for strategy in self.strategies:
            strategy.validate(connection, dao_factory, reserva)
