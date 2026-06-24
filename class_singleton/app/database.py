from .singleton_db import DatabaseSingleton


def get_db_connection():
    """Obtiene la conexión activa desde el Singleton."""
    return DatabaseSingleton().obtener_conexion()


def init_db():
    """Inicializa el esquema de la base de datos si no existe."""
    conn = get_db_connection()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS crud_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            operacion TEXT NOT NULL,
            item_id INTEGER,
            detalle TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    conn.commit()


def log_crud(operacion: str, item_id: int, detalle: str):
    """Registra las operaciones de CRUD en la base de datos."""
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO crud_logs (operacion, item_id, detalle) VALUES (?, ?, ?)",
        (operacion, item_id, detalle),
    )
    conn.commit()


def list_items():
    """Retorna la lista de todos los items en orden descendente."""
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT id, nombre, descripcion, created_at FROM items ORDER BY id DESC"
    ).fetchall()
    return [dict(row) for row in rows]


def get_item(item_id: int):
    """Recupera un item por su ID."""
    conn = get_db_connection()
    row = conn.execute(
        "SELECT id, nombre, descripcion, created_at FROM items WHERE id = ?",
        (item_id,),
    ).fetchone()
    return dict(row) if row else None


def create_item(nombre: str, descripcion: str) -> int:
    """Crea un nuevo item y registra la acción."""
    conn = get_db_connection()
    cursor = conn.execute(
        "INSERT INTO items (nombre, descripcion) VALUES (?, ?)",
        (nombre, descripcion),
    )
    conn.commit()
    new_id = cursor.lastrowid
    
    log_crud("CREATE", new_id, "Se creó un item")
    return new_id


def update_item(item_id: int, nombre: str, descripcion: str) -> bool:
    """Actualiza un item existente por su ID."""
    conn = get_db_connection()
    cursor = conn.execute(
        "UPDATE items SET nombre = ?, descripcion = ? WHERE id = ?",
        (nombre, descripcion, item_id),
    )
    conn.commit()
    updated = cursor.rowcount > 0
    
    if updated:
        log_crud("UPDATE", item_id, "Se actualizó un item")
    return updated


def delete_item(item_id: int) -> bool:
    """Elimina un item por su ID."""
    conn = get_db_connection()
    cursor = conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    
    if deleted:
        log_crud("DELETE", item_id, "Se eliminó un item")
    return deleted