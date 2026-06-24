import sqlite3

class DatabaseSingleton:
    _instancia = None
    
    def __new__(cls, db_path="app_data.sqlite3"):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._conexion = sqlite3.connect(db_path, check_same_thread=False)
            cls._instancia._conexion.row_factory = sqlite3.Row
            print(f"Conexión creada a {db_path}")
        else:
            print("Reutilizando conexión existente")
            
        return cls._instancia
        
    def obtener_conexion(self):
        """Devuelve la conexión única de la aplicación"""
        return self._conexion
        
    def cerrar(self):
        """Cierra la conexión y limpia la instancia"""
        if self._conexion:
            self._conexion.close()
            self._conexion = None
            DatabaseSingleton._instancia = None
            print("Conexión cerrada")