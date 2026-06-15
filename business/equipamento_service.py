# business/equipamento_service.py
from business.validation import BusinessException

class EquipamentoService:
    def __init__(self, connection_manager, dao_factory):
        self.connection_manager = connection_manager
        self.dao_factory = dao_factory

    def cadastrar_equipamento(self, equipamento):
        if not equipamento.nome or not equipamento.marca or not equipamento.num_serie or not equipamento.status:
            raise BusinessException("Nome, marca, número de série e status são obrigatórios.")
        if equipamento.status not in ('ATIVO', 'MANUTENCAO', 'INATIVO'):
            raise BusinessException("Status inválido. Escolha entre: ATIVO, MANUTENCAO, INATIVO.")

        conn = self.connection_manager.get_connection()
        try:
            # Check if laboratory exists (if laboratory_id is set)
            if equipamento.laboratorio_id:
                lab_dao = self.dao_factory.get_laboratorio_dao(conn)
                lab = lab_dao.find_by_id(equipamento.laboratorio_id)
                if not lab:
                    raise BusinessException(f"Laboratório associado com ID {equipamento.laboratorio_id} não existe.")

            equip_dao = self.dao_factory.get_equipamento_dao(conn)
            
            # Check unique serial number
            all_equip = equip_dao.find_all()
            for eq in all_equip:
                if eq.num_serie == equipamento.num_serie:
                    raise BusinessException(f"Já existe um equipamento cadastrado com o número de série: {equipamento.num_serie}")
                    
            return equip_dao.insert(equipamento)
        finally:
            conn.close()

    def listar_equipamentos(self):
        conn = self.connection_manager.get_connection()
        try:
            equip_dao = self.dao_factory.get_equipamento_dao(conn)
            return equip_dao.find_all()
        finally:
            conn.close()

    def buscar_equipamento_por_id(self, id_equipamento):
        conn = self.connection_manager.get_connection()
        try:
            equip_dao = self.dao_factory.get_equipamento_dao(conn)
            return equip_dao.find_by_id(id_equipamento)
        finally:
            conn.close()

    def atualizar_equipamento(self, equipamento):
        if not equipamento.id:
            raise BusinessException("ID do equipamento é necessário para atualização.")
        if not equipamento.nome or not equipamento.marca or not equipamento.num_serie or not equipamento.status:
            raise BusinessException("Nome, marca, número de série e status não podem ser nulos ou vazios.")
        if equipamento.status not in ('ATIVO', 'MANUTENCAO', 'INATIVO'):
            raise BusinessException("Status inválido. Escolha entre: ATIVO, MANUTENCAO, INATIVO.")

        conn = self.connection_manager.get_connection()
        try:
            # Check if laboratory exists (if laboratory_id is set)
            if equipamento.laboratorio_id:
                lab_dao = self.dao_factory.get_laboratorio_dao(conn)
                lab = lab_dao.find_by_id(equipamento.laboratorio_id)
                if not lab:
                    raise BusinessException(f"Laboratório associado com ID {equipamento.laboratorio_id} não existe.")

            equip_dao = self.dao_factory.get_equipamento_dao(conn)
            
            # Check unique serial number (excluding current)
            all_equip = equip_dao.find_all()
            for eq in all_equip:
                if eq.num_serie == equipamento.num_serie and eq.id != equipamento.id:
                    raise BusinessException(f"Já existe outro equipamento cadastrado com o número de série: {equipamento.num_serie}")
                    
            equip_dao.update(equipamento)
        finally:
            conn.close()

    def remover_equipamento(self, id_equipamento):
        conn = self.connection_manager.get_connection()
        try:
            equip_dao = self.dao_factory.get_equipamento_dao(conn)
            existing = equip_dao.find_by_id(id_equipamento)
            if not existing:
                raise BusinessException(f"Equipamento com ID {id_equipamento} não encontrado.")
            equip_dao.delete(id_equipamento)
        finally:
            conn.close()

    def listar_equipamentos_por_laboratorio(self, id_laboratorio):
        conn = self.connection_manager.get_connection()
        try:
            equip_dao = self.dao_factory.get_equipamento_dao(conn)
            return equip_dao.find_by_laboratorio(id_laboratorio)
        finally:
            conn.close()
