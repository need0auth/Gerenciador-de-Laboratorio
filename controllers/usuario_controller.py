# controllers/usuario_controller.py
from models.usuario import Usuario
from business.validation import BusinessException

class UsuarioController:
    def __init__(self, usuario_service):
        self.usuario_service = usuario_service

    def cadastrar(self, nome, email, senha, tipo):
        """
        Action to register a new user.
        """
        try:
            usuario = Usuario(nome=nome, email=email, senha=senha, tipo=tipo)
            usuario_salvo = self.usuario_service.cadastrar_usuario(usuario)
            return {
                "success": True,
                "message": "Usuário cadastrado com sucesso!",
                "data": usuario_salvo.to_dict()
            }
        except BusinessException as e:
            return {"success": False, "message": e.message}
        except Exception as e:
            return {"success": False, "message": f"Erro inesperado: {str(e)}"}

    def listar(self):
        """
        Action to retrieve all users.
        """
        try:
            usuarios = self.usuario_service.listar_usuarios()
            return {
                "success": True,
                "data": [u.to_dict() for u in usuarios]
            }
        except Exception as e:
            return {"success": False, "message": f"Erro ao listar usuários: {str(e)}"}

    def buscar_por_id(self, id_usuario):
        """
        Action to find a user by ID.
        """
        try:
            usuario = self.usuario_service.buscar_usuario_por_id(id_usuario)
            if usuario:
                return {
                    "success": True,
                    "data": usuario.to_dict()
                }
            return {"success": False, "message": f"Usuário com ID {id_usuario} não encontrado."}
        except Exception as e:
            return {"success": False, "message": f"Erro ao buscar usuário: {str(e)}"}

    def atualizar(self, id_usuario, nome, email, senha, tipo):
        """
        Action to update a user.
        """
        try:
            usuario = Usuario(id_usuario=id_usuario, nome=nome, email=email, senha=senha, tipo=tipo)
            self.usuario_service.atualizar_usuario(usuario)
            return {
                "success": True,
                "message": "Usuário atualizado com sucesso!"
            }
        except BusinessException as e:
            return {"success": False, "message": e.message}
        except Exception as e:
            return {"success": False, "message": f"Erro inesperado ao atualizar: {str(e)}"}

    def remover(self, id_usuario):
        """
        Action to delete a user.
        """
        try:
            self.usuario_service.remover_usuario(id_usuario)
            return {
                "success": True,
                "message": "Usuário removido com sucesso!"
            }
        except BusinessException as e:
            return {"success": False, "message": e.message}
        except Exception as e:
            return {"success": False, "message": f"Erro inesperado ao remover: {str(e)}"}
