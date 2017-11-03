from flask import render_template, flash, redirect, request, url_for
from app import app
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps

cliente = MongoClient(connect=False) 
db = cliente.base
user = {"nickname":"Mario"}

@app.route('/')
@app.route('/index')
def index():
    return render_template("home.html", user=user)

@app.route('/registrar', methods=['GET', 'POST'])
def registro():
    if request.method == 'GET':
        return render_template("form.html")

    else:
        validado = request.form.get("Valido","No valido")
        info = {"Titulo":request.form["Titulo"],
        "Contenido": request.form["Contenido"],
        "Valido": validado}
        db.info.insert_one(info)
        flash('Creado exitosamente')
        return redirect(url_for("lista"))

@app.route('/informacion')
def lista():
    return render_template("index.html",datos=db.info.find(),user=user)

@app.route('/detalle/<id>')
def detalle(id):
    detalle = db.info.find_one({"_id": ObjectId(id)})
    return render_template("detalle.html",dato=detalle,user=user)

@app.route('/revalidar/<id>')
def revalidar(id):
    detalle = db.info.find_one({"_id": ObjectId(id)})
    flash('Revalidado')
    if(detalle["Valido"] == "Valido"):
        result = db.info.update_one({"_id": ObjectId(id)},{"$set": {"Valido": "No Valido"}})
    else:
        result = db.info.update_one({"_id": ObjectId(id)},{"$set": {"Valido": "Valido"}})
    return redirect(url_for("lista"))

@app.route('/eliminar/<id>')
def eliminar(id):
    detalle = db.info.delete_one({"_id": ObjectId(id)})
    flash('Eliminado exitosamente')
    return redirect(url_for("lista"))