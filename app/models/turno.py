from app.database import Database

class Turno:
    @staticmethod
    def create(laboratorio_id, dia_semana, hora_inicio, hora_fin):
        db = Database()
        query = """
            INSERT INTO turnos (laboratorio_id, dia_semana, hora_inicio, hora_fin)
            VALUES (%s, %s, %s, %s)
        """
        return db.execute_query(query, (laboratorio_id, dia_semana, hora_inicio, hora_fin), return_lastrowid=True)

    @staticmethod
    def get_by_laboratorio(laboratorio_id):
        db = Database()
        query = "SELECT * FROM turnos WHERE laboratorio_id = %s ORDER BY dia_semana, hora_inicio"
        return db.fetch_all(query, (laboratorio_id,))