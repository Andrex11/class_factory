from datetime import datetime
from flask import jsonify, render_template, request
from . import app
from .database import (
    create_item,
    delete_item,
    get_item,
    list_items,
    update_item,
)


def funcion_python_basica() -> str:
    return f"Hola desde Python. Hora del servidor: {datetime.now().strftime('%H:%M:%S')}"


def leer_payload() -> tuple[str, str]:
    payload = request.get_json(silent=True) or {}
    nombre = payload.get("nombre", "").strip()
    descripcion = payload.get("descripcion", "").strip()
    return nombre, descripcion


def render_home(resultado: str = "", registros: list = None):
    if registros is None:
        registros = []
    return render_template("index.html", resultado=resultado, registros=registros)


@app.route("/", methods=["GET"])
def home():
    return render_home("Selecciona una acción del formulario.")


@app.route("/operar", methods=["POST"])
def operar_formulario():
    accion = request.form.get("accion", "").strip().lower()
    item_id = request.form.get("id", "").strip()
    nombre = request.form.get("nombre", "").strip()
    descripcion = request.form.get("descripcion", "").strip()

    if accion == "registrar":
        if not nombre:
            return render_home("Error: nombre es obligatorio.")
        new_id = create_item(nombre, descripcion)
        return render_home(f"Registro creado con ID {new_id}.")

    if accion == "seleccionar":
        if not item_id:
            return render_home("Error: ingresa un ID para seleccionar.")
        item = get_item(int(item_id))
        return render_home(f"Item encontrado: {item}" if item else "Item no encontrado.")

    if accion == "actualizar":
        if not item_id or not nombre:
            return render_home("Error: ID y nombre son obligatorios para actualizar.")
        if update_item(int(item_id), nombre, descripcion):
            return render_home(f"Item {item_id} actualizado.")
        return render_home("Item no encontrado para actualizar.")

    if accion == "eliminar":
        if not item_id:
            return render_home("Error: ingresa un ID para eliminar.")
        if delete_item(int(item_id)):
            return render_home(f"Item {item_id} eliminado.")
        return render_home("Item no encontrado para eliminar.")

    if accion == "listar":
        return render_home("Listado de registros:", list_items())

    return render_home("Acción no válida.")


# --- API ENDPOINTS ---

@app.route("/api/saludo", methods=["GET"])
def saludo():
    return jsonify({"mensaje": funcion_python_basica()})


@app.route("/items", methods=["GET"])
def items_list():
    return jsonify(list_items())


@app.route("/items/<int:item_id>", methods=["GET"])
def items_get(item_id: int):
    item = get_item(item_id)
    if item is None:
        return jsonify({"error": "Item no encontrado"}), 404
    return jsonify(item)


@app.route("/items", methods=["POST"])
def items_create():
    nombre, descripcion = leer_payload()
    if not nombre:
        return jsonify({"error": "El campo 'nombre' es obligatorio"}), 400

    item_id = create_item(nombre, descripcion)
    return jsonify({"message": "Item creado", "id": item_id}), 201


@app.route("/items/<int:item_id>", methods=["PUT"])
def items_update(item_id: int):
    nombre, descripcion = leer_payload()
    if not nombre:
        return jsonify({"error": "El campo 'nombre' es obligatorio"}), 400

    if not update_item(item_id, nombre, descripcion):
        return jsonify({"error": "Item no encontrado"}), 404
    return jsonify({"message": "Item actualizado", "id": item_id})


@app.route("/items/<int:item_id>", methods=["DELETE"])
def items_delete(item_id: int):
    if not delete_item(item_id):
        return jsonify({"error": "Item no encontrado"}), 404
    return jsonify({"message": "Item eliminado", "id": item_id})