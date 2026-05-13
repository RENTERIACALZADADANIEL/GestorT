import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde la raíz del proyecto
load_dotenv()

class Database:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection = None
        return cls._instance
    
    def connect(self):
        """Establece la conexión a la base de datos"""
        try:
            if self.connection is None or not self.connection.is_connected():
                self.connection = mysql.connector.connect(
                    host=os.getenv('DB_HOST', 'localhost'),
                    user=os.getenv('DB_USER', 'root'),
                    password=os.getenv('DB_PASSWORD', ''),
                    database=os.getenv('DB_NAME', 'gestor_db'),
                    port=os.getenv('DB_PORT', 3306)
                )
            return self.connection
        except Error as e:
            print(f"Error al conectar a MySQL: {e}")
            return None
    
    def disconnect(self):
        """Cierra la conexión a la base de datos"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def execute_query(self, query, params=None):
        """Ejecuta una consulta SELECT y retorna los resultados"""
        connection = self.connect()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute(query, params or ())
                result = cursor.fetchall()
                cursor.close()
                return result
            except Error as e:
                print(f"Error en la consulta: {e}")
                return None
        return None
    
    def execute_insert(self, query, params=None):
        """Ejecuta INSERT/UPDATE/DELETE y retorna el ID o número de filas afectadas"""
        connection = self.connect()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(query, params or ())
                connection.commit()
                last_id = cursor.lastrowid
                rows_affected = cursor.rowcount
                cursor.close()
                return last_id if last_id else rows_affected
            except Error as e:
                print(f"Error en la inserción: {e}")
                connection.rollback()
                return None
        return None