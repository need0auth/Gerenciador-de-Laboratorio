# dao/laboratorio_dao.py
from dao.base_dao import BaseDAO
from models.laboratorio import Laboratorio

class LaboratorioDAO(BaseDAO):
    def insert(self, laboratorio):
        """
        Inserts a new laboratory and sets the generated ID.
        """
        sql = "INSERT INTO laboratorios (nome, sala, capacidade, descricao) VALUES (%s, %s, %s, %s) RETURNING id;"
        with self.connection.cursor() as cur:
            cur.execute(sql, (laboratorio.nome, laboratorio.sala, laboratorio.capacidade, laboratorio.descricao))
            laboratorio.id = cur.fetchone()[0]
        self.connection.commit()
        return laboratorio

    def find_by_id(self, id_laboratorio):
        """
        Finds a laboratory by ID.
        """
        sql = "SELECT id, nome, sala, capacidade, descricao FROM laboratorios WHERE id = %s;"
        with self.connection.cursor() as cur:
            cur.execute(sql, (id_laboratorio,))
            row = cur.fetchone()
            if row:
                return Laboratorio(id_laboratorio=row[0], nome=row[1], sala=row[2], capacidade=row[3], descricao=row[4])
        return None

    def find_all(self):
        """
        Returns all laboratories.
        """
        sql = "SELECT id, nome, sala, capacidade, descricao FROM laboratorios ORDER BY nome;"
        laboratorios = []
        with self.connection.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
            for row in rows:
                laboratorios.append(Laboratorio(id_laboratorio=row[0], nome=row[1], sala=row[2], capacidade=row[3], descricao=row[4]))
        return laboratorios

    def update(self, laboratorio):
        """
        Updates an existing laboratory.
        """
        sql = "UPDATE laboratorios SET nome = %s, sala = %s, capacidade = %s, descricao = %s WHERE id = %s;"
        with self.connection.cursor() as cur:
            cur.execute(sql, (laboratorio.nome, laboratorio.sala, laboratorio.capacidade, laboratorio.descricao, laboratorio.id))
        self.connection.commit()

    def delete(self, id_laboratorio):
        """
        Deletes a laboratory by ID.
        """
        sql = "DELETE FROM laboratorios WHERE id = %s;"
        with self.connection.cursor() as cur:
            cur.execute(sql, (id_laboratorio,))
        self.connection.commit()

    def get_related_equipments(self, id_laboratorio):
        """
        Queries all equipment related to this laboratory (related data query).
        """
        from models.equipamento import Equipamento
        sql = "SELECT id, nome, marca, num_serie, laboratorio_id, status FROM equipamentos WHERE laboratorio_id = %s;"
        equipamentos = []
        with self.connection.cursor() as cur:
            cur.execute(sql, (id_laboratorio,))
            rows = cur.fetchall()
            for row in rows:
                equipamentos.append(Equipamento(id_equipamento=row[0], nome=row[1], marca=row[2], num_serie=row[3], laboratorio_id=row[4], status=row[5]))
        return equipamentos

    def get_related_reservations(self, id_laboratorio):
        """
        Queries all reservations related to this laboratory (related data query).
        """
        from models.reserva import Reserva
        sql = "SELECT id, laboratorio_id, usuario_id, data_inicio, data_fim, finalidade, status FROM reservas WHERE laboratorio_id = %s ORDER BY data_inicio;"
        reservas = []
        with self.connection.cursor() as cur:
            cur.execute(sql, (id_laboratorio,))
            rows = cur.fetchall()
            for row in rows:
                reservas.append(Reserva(id_reserva=row[0], laboratorio_id=row[1], usuario_id=row[2], data_inicio=row[3], data_fim=row[4], finalidade=row[5], status=row[6]))
        return reservas
