from flask import Flask
from .database import init_db
from .singleton_db  import DatabaseSingleton

app = Flask(__name__)
app.config["DATABASE_PATH"] = "app_data.sqlite3"

with app.app_context():
    # Inicializamos la instancia Singleton con la ruta configurada
    DatabaseSingleton(app.config["DATABASE_PATH"])
    init_db()

# Importación al final para evitar problemas de importación circular
from . import routes  # noqa: E402, F401D