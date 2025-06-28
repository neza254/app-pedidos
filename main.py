from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)
ARCHIVO = "pedidos.json"

def cargar():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r") as f:
            return json.load(f)
    return []

def guardar(pedidos):
    with open(ARCHIVO, "w") as f:
        json.dump(pedidos, f, indent=4)

@app.route("/")
def index():
    pedidos = cargar()
    return render_template("index.html", pedidos=pedidos)

@app.route("/agregar", methods=["POST"])
def agregar():
    cliente = request.form["cliente"]
    productos = request.form.getlist("producto")
    cantidades = request.form.getlist("cantidad")
    precios = request.form.getlist("precio")

    lista_productos = []
    total_pedido = 0

    for p, c, pr in zip(productos, cantidades, precios):
        if p and c.isdigit() and pr:
            c = int(c)
            pr = float(pr)
            total = c * pr
            total_pedido += total
            lista_productos.append({
                "producto": p,
                "cantidad": c,
                "precio": pr,
                "total": total
            })

    pedido = {
        "cliente": cliente,
        "productos": lista_productos,
        "total": total_pedido
    }

    pedidos = cargar()
    pedidos.append(pedido)
    guardar(pedidos)
    return redirect("/")

@app.route("/borrar/<int:indice>", methods=["POST"])
def borrar(indice):
    pedidos = cargar()
    if 0 <= indice < len(pedidos):
        pedidos.pop(indice)
        guardar(pedidos)
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
