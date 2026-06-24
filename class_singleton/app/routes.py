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


def db_path():
    return app.config["DATABASE_PATH"]


def funcion_python_basica():
    return f"Hola desde Python. Hora del servidor: {datetime.now().strftime('%H:%M:%S')}"


def leer_payload():
    payload = request.get_json(silent=True) or {}
    nombre = payload.get("nombre", "").strip()
    descripcion = payload.get("descripcion", "").strip()
    return nombre, descripcion


def render_home(resultado="", registros=None):
    if registros is None:
        registros = []
    return render_template("index.html", resultado=resultado, registros=registros)

def registrar_item(nombre, descripcion):

    if not nombre:
        return render_home(
            "Error: nombre es obligatorio."
        )

    new_id = create_item(
        db_path(),
        nombre,
        descripcion
    )

    return render_home(
        f"Registro creado con ID {new_id}."
    )

def seleccionar_item_form(item_id):

    if not item_id:
        return render_home(
            "Error: ingresa un ID para seleccionar."
        )

    item = get_item(
        db_path(),
        int(item_id)
    )

    if item is None:
        return render_home(
            "Item no encontrado."
        )

    return render_home(
        f"Item encontrado: {item}"
    )

def actualizar_item_form(
    item_id,
    nombre,
    descripcion
):

    if not item_id:
        return render_home(
            "Error: ingresa un ID para actualizar."
        )

    if not nombre:
        return render_home(
            "Error: nombre es obligatorio."
        )

    updated = update_item(
        db_path(),
        int(item_id),
        nombre,
        descripcion
    )

    if not updated:
        return render_home(
            "Item no encontrado para actualizar."
        )

    return render_home(
        f"Item {item_id} actualizado."
    )

def eliminar_item_form(item_id):

    if not item_id:
        return render_home(
            "Error: ingresa un ID para eliminar."
        )

    deleted = delete_item(
        db_path(),
        int(item_id)
    )

    if not deleted:
        return render_home(
            "Item no encontrado para eliminar."
        )

    return render_home(
        f"Item {item_id} eliminado."
    )

def listar_items_form():

    registros = list_items(
        db_path()
    )

    return render_home(
        "Listado de registros:",
        registros
    )

@app.route("/", methods=["GET"])
def home():
    return render_home("Selecciona una accion del formulario.")


@app.route("/operar", methods=["POST"])
def operar_formulario():
    accion = request.form.get("accion", "").strip().lower()
    item_id = request.form.get("id", "").strip()
    nombre = request.form.get("nombre", "").strip()
    descripcion = request.form.get("descripcion", "").strip()

    if accion == "registrar":
        if not nombre:
            return render_home("Error: nombre es obligatorio.")
        new_id = create_item(db_path(), nombre, descripcion)
        return render_home(f"Registro creado con ID {new_id}.")

    if accion == "seleccionar":
        if not item_id:
            return render_home("Error: ingresa un ID para seleccionar.")
        item = get_item(db_path(), int(item_id))
        if item is None:
            return render_home("Item no encontrado.")
        return render_home(f"Item encontrado: {item}")

    if accion == "actualizar":
        if not item_id:
            return render_home("Error: ingresa un ID para actualizar.")
        if not nombre:
            return render_home("Error: nombre es obligatorio para actualizar.")
        updated = update_item(db_path(), int(item_id), nombre, descripcion)
        if not updated:
            return render_home("Item no encontrado para actualizar.")
        return render_home(f"Item {item_id} actualizado.")

    if accion == "eliminar":
        if not item_id:
            return render_home("Error: ingresa un ID para eliminar.")
        deleted = delete_item(db_path(), int(item_id))
        if not deleted:
            return render_home("Item no encontrado para eliminar.")
        return render_home(f"Item {item_id} eliminado.")

    if accion == "listar":
        registros = list_items(db_path())
        return render_home("Listado de registros:", registros)

    return render_home("Accion no valida.")


@app.route("/api/saludo", methods=["GET"])
def saludo():
    mensaje = funcion_python_basica()
    return jsonify({"mensaje": mensaje})


@app.route("/items", methods=["GET"])
def items_list():
    return jsonify(list_items(db_path()))


@app.route("/items/<int:item_id>", methods=["GET"])
def items_get(item_id: int):
    item = get_item(db_path(), item_id)
    if item is None:
        return jsonify({"error": "Item no encontrado"}), 404
    return jsonify(item)


@app.route("/items", methods=["POST"])
def items_create():
    nombre, descripcion = leer_payload()

    if not nombre:
        return jsonify({"error": "El campo 'nombre' es obligatorio"}), 400

    item_id = create_item(db_path(), nombre, descripcion)
    return jsonify({"message": "Item creado", "id": item_id}), 201


@app.route("/items/<int:item_id>", methods=["PUT"])
def items_update(item_id: int):
    nombre, descripcion = leer_payload()

    if not nombre:
        return jsonify({"error": "El campo 'nombre' es obligatorio"}), 400

    updated = update_item(db_path(), item_id, nombre, descripcion)
    if not updated:
        return jsonify({"error": "Item no encontrado"}), 404

    return jsonify({"message": "Item actualizado", "id": item_id})


@app.route("/items/<int:item_id>", methods=["DELETE"])
def items_delete(item_id: int):
    deleted = delete_item(db_path(), item_id)
    if not deleted:
        return jsonify({"error": "Item no encontrado"}), 404

    return jsonify({"message": "Item eliminado", "id": item_id})
