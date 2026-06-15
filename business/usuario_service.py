# business/usuario_service.py
from business.validation import BusinessException

class UsuarioService:
    def __init__(self, connection_manager, dao_factory):
        self.connection_manager = connection_manager
        self.dao_factory = dao_factory

    def cadastrar_usuario(self, usuario):
        """
        Validates and registers a new user.
        """
        if not usuario.nome or not usuario.email or not usuario.senha or not usuario.tipo:
            raise BusinessException("Nome, email, senha e tipo do usuário são campos obrigatórios.")
        
        conn = self.connection_manager.get_connection()
        try:
            user_dao = self.dao_factory.get_usuario_dao(conn)
            
            # Check if email is already in use
            existing = user_dao.find_by_email(usuario.email)
            if existing:
                raise BusinessException(f"Já existe um usuário cadastrado com o e-mail: {usuario.email}")
            
            return user_dao.insert(usuario)
        finally:
            conn.close()

    def listar_usuarios(self):
        conn = self.connection_manager.get_connection()
        try:
            user_dao = self.dao_factory.get_usuario_dao(conn)
            return user_dao.find_all()
        finally:
            conn.close()

    def buscar_usuario_por_id(self, id_usuario):
        conn = self.connection_manager.get_connection()
        try:
            user_dao = self.dao_factory.get_usuario_dao(conn)
            return user_dao.find_by_id(id_usuario)
        finally:
            conn.close()

    def atualizar_usuario(self, usuario):
        if not usuario.id:
            raise BusinessException("ID do usuário é necessário para atualização.")
        if not usuario.nome or not usuario.email or not usuario.senha or not usuario.tipo:
            raise BusinessException("Nome, email, senha e tipo do usuário não podem ser vazios.")
            
        conn = self.connection_manager.get_connection()
        try:
            user_dao = self.dao_factory.get_usuario_dao(conn)
            
            # Check if email is in use by another user
            existing = user_dao.find_by_email(usuario.email)
            if existing and existing.id != usuario.id:
                raise BusinessException(f"O e-mail {usuario.email} já está sendo usado por outro usuário.")
                
            user_dao.update(usuario)
        finally:
            conn.close()

    def remover_usuario(self, id_usuario):
        conn = self.connection_manager.get_connection()
        try:
            user_dao = self.dao_factory.get_usuario_dao(conn)
            existing = user_dao.find_by_id(id_usuario)
            if not existing:
                raise BusinessException(f"Usuário com ID {id_usuario} não encontrado.")
            user_dao.delete(id_usuario)
        finally:
            conn.close()
