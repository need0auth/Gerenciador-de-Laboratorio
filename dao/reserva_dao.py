# dao/reserva_dao.py
from dao.base_dao import BaseDAO
from models.reserva import Reserva

class ReservaDAO(BaseDAO):
    def insert(self, reserva):
        """
        Inserts a new reservation and sets the generated ID.
        """
        sql = """
            INSERT INTO reservas (laboratorio_id, usuario_id, data_inicio, data_fim, finalidade, status)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
        """
        with self.connection.cursor() as cur:
            cur.execute(sql, (reserva.laboratorio_id, reserva.usuario_id, reserva.data_inicio, reserva.data_fim, reserva.finalidade, reserva.status))
            reserva.id = cur.fetchone()[0]
        self.connection.commit()
        return reserva

    def find_by_id(self, id_reserva):
        """
        Finds a reservation by ID.
        """
        sql = "SELECT id, laboratorio_id, usuario_id, data_inicio, data_fim, finalidade, status FROM reservas WHERE id = %s;"
        with self.connection.cursor() as cur:
            cur.execute(sql, (id_reserva,))
            row = cur.fetchone()
            if row:
                return Reserva(id_reserva=row[0], laboratorio_id=row[1], usuario_id=row[2], data_inicio=row[3], data_fim=row[4], finalidade=row[5], status=row[6])
        return None

    def find_all(self):
        """
        Returns all reservations.
        """
        sql = "SELECT id, laboratorio_id, usuario_id, data_inicio, data_fim, finalidade, status FROM reservas ORDER BY data_inicio;"
        reservas = []
        with self.connection.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
            for row in rows:
                reservas.append(Reserva(id_reserva=row[0], laboratorio_id=row[1], usuario_id=row[2], data_inicio=row[3], data_fim=row[4], finalidade=row[5], status=row[6]))
        return reservas

    def update(self, reserva):
        """
        Updates an existing reservation.
        """
        sql = """
            UPDATE reservas SET laboratorio_id = %s, usuario_id = %s, data_inicio = %s, data_fim = %s, finalidade = %s, status = %s
            WHERE id = %s;
        """
        with self.connection.cursor() as cur:
            cur.execute(sql, (reserva.laboratorio_id, reserva.usuario_id, reserva.data_inicio, reserva.data_fim, reserva.finalidade, reserva.status, reserva.id))
        self.connection.commit()

    def delete(self, id_reserva):
        """
        Deletes a reservation by ID.
        """
        sql = "DELETE FROM reservas WHERE id = %s;"
        with self.connection.cursor() as cur:
            cur.execute(sql, (id_reserva,))
        self.connection.commit()

    def find_conflicting_reservations(self, laboratorio_id, data_inicio, data_fim, exclude_id=None):
        """
        Checks if there are any approved reservations for the same laboratory overlapping with the given timeframe.
        Overlaps check: (start1 < end2) AND (end1 > start2)
        """
        sql = """
            SELECT id, laboratorio_id, usuario_id, data_inicio, data_fim, finalidade, status
            FROM reservas
            WHERE laboratorio_id = %s
              AND status = 'APROVADA'
              AND (data_inicio < %s) AND (data_fim > %s)
        """
        params = [laboratorio_id, data_fim, data_inicio]
        if exclude_id is not None:
            sql += " AND id <> %s"
            params.append(exclude_id)

        sql += ";"
        reservas = []
        with self.connection.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
            for row in rows:
                reservas.append(Reserva(id_reserva=row[0], laboratorio_id=row[1], usuario_id=row[2], data_inicio=row[3], data_fim=row[4], finalidade=row[5], status=row[6]))
        return reservas

    def get_related_usuario(self, id_reserva):
        """
        Fetches the user details related to the reservation (related data query).
        """
        from models.usuario import Usuario
        sql = """
            SELECT u.id, u.nome, u.email, u.senha, u.tipo
            FROM usuarios u
            JOIN reservas r ON r.usuario_id = u.id
            WHERE r.id = %s;
        """
        with self.connection.cursor() as cur:
            cur.execute(sql, (id_reserva,))
            row = cur.fetchone()
            if row:
                return Usuario(id_usuario=row[0], nome=row[1], email=row[2], senha=row[3], tipo=row[4])
        return None

    def get_related_laboratorio(self, id_reserva):
        """
        Fetches the laboratory details related to the reservation (related data query).
        """
        from models.laboratorio import Laboratorio
        sql = """
            SELECT l.id, l.nome, l.sala, l.capacidade, l.descricao
            FROM laboratorios l
            JOIN reservas r ON r.laboratorio_id = l.id
            WHERE r.id = %s;
        """
        with self.connection.cursor() as cur:
            cur.execute(sql, (id_reserva,))
            row = cur.fetchone()
            if row:
                return Laboratorio(id_laboratorio=row[0], nome=row[1], sala=row[2], capacidade=row[3], descricao=row[4])
        return None
