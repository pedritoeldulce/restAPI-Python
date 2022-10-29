from crypt import methods
import json
from flask import Flask, jsonify, request

app = Flask(__name__)

from products import products


@app.route("/ping")
def ping():
    return jsonify({"mensaje":"pong"})

@app.route("/products", methods=["GET"])
def getProducts():
    return jsonify({"products":products, "message":"Ok"})


@app.route("/products/<string:product_name>")
def getProduct(product_name):
    getProduct = list(filter(lambda p: p["name"] == product_name, products))
    
    if not getProduct:
        return jsonify({"message":"Producto no encontrado"})

    return jsonify({"product":getProduct})

@app.route("/products", methods=["POST"])
def addProduct():
    new_product = {
        "name": request.json["name"],
        "price": request.json["price"],
        "quantity": request.json["quantity"]
    }

    products.append(new_product)

    return jsonify({"Products": products, "message":"Product add"})

@app.route("/products/<string:product_name>", methods=["PUT"])
def editProduct(product_name):
    productFound = list(filter(lambda p: p["name"] == product_name, products))
    
    
    if productFound:
        # Estamos simulando el update, en una BD real es diferente, pero la idea es la misma
        productFound[0]['name'] = request.json['name']
        productFound[0]['price'] = request.json['price']
        productFound[0]['quantity'] = request.json["quantity"]
        
        return jsonify({"products": products, "message":"Product Update"}) 
    return jsonify({"message":"Product not Found"})

@app.route("/products/<string:product_name>", methods=["DELETE"])
def deleteProduct(product_name):
    #busqueda del producto por su nombre
    productFound = list(filter(lambda p: p["name"] == product_name, products))

    if productFound:
        products.remove(productFound[0])
        return jsonify({"products": products, "message":"Producto eliminado"})

    return jsonify({"message":"producto not Found"})

if __name__== '__main__':
    app.run(debug=True, port=4000)