from flask import Flask, jsonify, request

app = Flask(__name__)

# Lista inicial de productos
productos = [
    {"id": 1, "nombre": "Laptop",  "precio": 5500},
    {"id": 2, "nombre": "Mouse",   "precio": 150},
    {"id": 3, "nombre": "Teclado", "precio": 250}
]

@app.route("/")
def home():
    return "Bienvenido al sistema de productos"

@app.route("/acerca")
def acerca():
    return jsonify({
        "aplicacion": "Gestión de Productos",
        "version": 1.0,
        "autor": "Tu Nombre"
    })

# === RUTAS DEL EJERCICIO 2 ===

# 1) GET /productos  → devuelve todos los productos
@app.route("/productos", methods=["GET"])
def get_productos():
    return jsonify(productos)

# 2) GET /productos/<id> → devuelve un producto por id o error 404
@app.route("/productos/<int:id>", methods=["GET"])
def get_producto(id):
    prod = next((p for p in productos if p["id"] == id), None)
    if prod is None:
        return jsonify({"error": "Producto no encontrado"}), 404
    return jsonify(prod)

# 3) POST /productos → inserta un nuevo producto (JSON con nombre y precio)
@app.route("/productos", methods=["POST"])
def add_producto():
    data = request.get_json(silent=True) or {}
    nombre = data.get("nombre")
    precio = data.get("precio")

    # Validaciones simples
    if not isinstance(nombre, str) or nombre.strip() == "":
        return jsonify({"error": "Nombre inválido"}), 400
    if not isinstance(precio, (int, float)):
        return jsonify({"error": "Precio inválido"}), 400

    nuevo_id = (max((p["id"] for p in productos), default=0) + 1)
    nuevo = {"id": nuevo_id, "nombre": nombre.strip(), "precio": precio}
    productos.append(nuevo)

    # Lo que exige el examen: confirmar con mensaje
    return jsonify({"mensaje": "Producto agregado correctamente"}), 201

# 4) DELETE /productos/<id> → elimina por id o error 404
@app.route("/productos/<int:id>", methods=["DELETE"])
def delete_producto(id):
    idx = next((i for i, p in enumerate(productos) if p["id"] == id), None)
    if idx is None:
        return jsonify({"error": "Producto no encontrado"}), 404
    productos.pop(idx)
    return jsonify({"mensaje": "Producto eliminado correctamente"})
    # (status 200 por simplicidad)

if __name__ == "__main__":
    app.run(debug=True)

