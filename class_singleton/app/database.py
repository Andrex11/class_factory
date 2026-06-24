import sqlite3


def get_db_connection(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def execute_query(db_path, query, params=(), commit=False):
    conn = get_db_connection(db_path)

    try:
        cursor = conn.execute(query, params)

        if commit:
            conn.commit()

        return cursor

    finally:
        conn.close()


def init_db(db_path):
    conn = get_db_connection(db_path)

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
    conn.close()


def log_crud(db_path, operacion, item_id, detalle):
    conn = get_db_connection(db_path)

    conn.execute(
        """
        INSERT INTO crud_logs
        (operacion, item_id, detalle)
        VALUES (?, ?, ?)
        """,
        (operacion, item_id, detalle),
    )

    conn.commit()
    conn.close()


def list_items(db_path):
    conn = get_db_connection(db_path)

    rows = conn.execute(
        """
        SELECT
            id,
            nombre,
            descripcion,
            created_at
        FROM items
        ORDER BY id DESC
        """
    ).fetchall()

    conn.close()

    return [dict(row) for row in rows]


def get_item(db_path, item_id):
    conn = get_db_connection(db_path)

    row = conn.execute(
        """
        SELECT
            id,
            nombre,
            descripcion,
            created_at
        FROM items
        WHERE id = ?
        """,
        (item_id,),
    ).fetchone()

    conn.close()

    return dict(row) if row else None


def create_item(db_path, nombre, descripcion):
    conn = get_db_connection(db_path)

    cursor = conn.execute(
        """
        INSERT INTO items
        (nombre, descripcion)
        VALUES (?, ?)
        """,
        (nombre, descripcion),
    )

    conn.commit()

    new_id = cursor.lastrowid

    conn.close()

    log_crud(
        db_path,
        "CREATE",
        new_id,
        "Se creo un item"
    )

    return new_id


def update_item(db_path, item_id, nombre, descripcion):
    conn = get_db_connection(db_path)

    cursor = conn.execute(
        """
        UPDATE items
        SET nombre = ?, descripcion = ?
        WHERE id = ?
        """,
        (nombre, descripcion, item_id),
    )

    conn.commit()

    updated = cursor.rowcount > 0

    conn.close()

    if updated:
        log_crud(
            db_path,
            "UPDATE",
            item_id,
            "Se actualizo un item"
        )

    return updated


def delete_item(db_path, item_id):
    conn = get_db_connection(db_path)

    cursor = conn.execute(
        """
        DELETE FROM items
        WHERE id = ?
        """,
        (item_id,),
    )

    conn.commit()

    deleted = cursor.rowcount > 0

    conn.close()

    if deleted:
        log_crud(
            db_path,
            "DELETE",
            item_id,
            "Se elimino un item"
        )

    return deleted