# dao/equipamento_dao.py
from dao.base_dao import BaseDAO
from models.equipamento import Equipamento

class EquipamentoDAO(BaseDAO):
    def insert(self, equipamento):
        """
        Inserts a new equipment and sets the generated ID.
        """
        sql = "INSERT INTO equipamentos (nome, marca, num_serie, laboratorio_id, status) VALUES (%s, %s, %s, %s, %s) RETURNING id;"
        with self.connection.cursor() as cur:
            cur.execute(sql, (equipamento.nome, equipamento.marca, equipamento.num_serie, equipamento.laboratorio_id, equipamento.status))
            equipamento.id = cur.fetchone()[0]
        self.connection.commit()
        return equipamento

    def find_by_id(self, id_equipamento):
        """
        Finds equipment by ID.
        """
        sql = "SELECT id, nome, marca, num_serie, laboratorio_id, status FROM equipamentos WHERE id = %s;"
        with self.connection.cursor() as cur:
            cur.execute(sql, (id_equipamento,))
            row = cur.fetchone()
            if row:
                return Equipamento(id_equipamento=row[0], nome=row[1], marca=row[2], num_serie=row[3], laboratorio_id=row[4], status=row[5])
        return None

    def find_all(self):
        """
        Returns all equipment.
        """
        sql = "SELECT id, nome, marca, num_serie, laboratorio_id, status FROM equipamentos ORDER BY nome;"
        equipamentos = []
        with self.connection.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
            for row in rows:
                equipamentos.append(Equipamento(id_equipamento=row[0], nome=row[1], marca=row[2], num_serie=row[3], laboratorio_id=row[4], status=row[5]))
        return equipamentos

    def update(self, equipamento):
        """
        Updates an existing equipment.
        """
        sql = "UPDATE equipamentos SET nome = %s, marca = %s, num_serie = %s, laboratorio_id = %s, status = %s WHERE id = %s;"
        with self.connection.cursor() as cur:
            cur.execute(sql, (equipamento.nome, equipamento.marca, equipamento.num_serie, equipamento.laboratorio_id, equipamento.status, equipamento.id))
        self.connection.commit()

    def delete(self, id_equipamento):
        """
        Deletes equipment by ID.
        """
        sql = "DELETE FROM equipamentos WHERE id = %s;"
        with self.connection.cursor() as cur:
            cur.execute(sql, (id_equipamento,))
        self.connection.commit()

    def find_by_laboratorio(self, id_laboratorio):
        """
        Finds all equipment associated with a specific laboratory.
        """
        sql = "SELECT id, nome, marca, num_serie, laboratorio_id, status FROM equipamentos WHERE laboratorio_id = %s ORDER BY nome;"
        equipamentos = []
        with self.connection.cursor() as cur:
            cur.execute(sql, (id_laboratorio,))
            rows = cur.fetchall()
            for row in rows:
                equipamentos.append(Equipamento(id_equipamento=row[0], nome=row[1], marca=row[2], num_serie=row[3], laboratorio_id=row[4], status=row[5]))
        return equipamentos
