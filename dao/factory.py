# dao/factory.py
from dao.usuario_dao import UsuarioDAO
from dao.laboratorio_dao import LaboratorioDAO
from dao.equipamento_dao import EquipamentoDAO
from dao.reserva_dao import ReservaDAO

class DAOFactory:
    def __init__(self):
        # Initializer for the factory instance
        pass

    def get_usuario_dao(self, connection):
        """
        Factory method for UsuarioDAO.
        """
        return UsuarioDAO(connection)

    def get_laboratorio_dao(self, connection):
        """
        Factory method for LaboratorioDAO.
        """
        return LaboratorioDAO(connection)

    def get_equipamento_dao(self, connection):
        """
        Factory method for EquipamentoDAO.
        """
        return EquipamentoDAO(connection)

    def get_reserva_dao(self, connection):
        """
        Factory method for ReservaDAO.
        """
        return ReservaDAO(connection)
