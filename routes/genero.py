from flask import request
from app import app, db
from models.genero import *
from sqlalchemy import exc

@app.route("/genero/", methods=['GET'])
def listarGeneros():
    try:
        mensaje=None
        listaGeneros=[]
        if request.method=="GET":
            generos = Genero.query.order_by(Genero.idGenero).all()
            
            for g in generos:
                genero={
                    "id": g.idGenero,
                    "nombre": g.genNombre
                }
                listaGeneros.append(genero)
        else:
            mensaje="Tarea no permitida"
    except exc.SQLAlchemyError as error:
        mensaje=str(error)
        
    return {"mensaje": mensaje, "generos": listaGeneros}


@app.route("/genero/", methods=['POST'])
def addGenero():
    try:
        mensaje=None
        estado=False
        if request.method=='POST':
            datos = request.get_json(force=True)
            genero = Genero(genNombre = datos['genero'])
            db.session.add(genero)
            db.session.commit()
            estado=True
            mensaje=f"Genero Agregado Correctamente con id: {genero.idGenero}"
        else:
            mensaje="Tarea no permitida"      
    except exc.SQLAlchemyError as error:
        db.session.rollback()
        mensaje=str(error)
        
    return {"estado": estado, "mensaje":mensaje}

@app.route("/genero/", methods=['PUT'])
def updateGenero():
    try:
        estado=False
        mensaje=None
        if request.method=='PUT':
            datos = request.get_json(force=True)
            genero = Genero.query.get(int(datos['id']))
            #actualiza nombre de genero con el nombre que llegue
            genero.genNombre = datos['nombre']
            db.session.commit()
            estado=True
            mensaje="Genero Actualizado Correctamente"
        else:
            mensaje="Tarea no permitida"
    except exc.SQLAlchemyError as error:
        db.session.rollback()
        mensaje=str(error)
        
    return {"estado": estado, "mensaje":mensaje}


@app.route("/genero/", methods=['DELETE'])
def deleteGenero():
    try:
        estado=False
        mensaje=None
        if request.method=='DELETE':
            datos=request.get_json(force=True)
            generoAEliminar = Genero.query.get(int(datos['id']))
            db.session.delete(generoAEliminar)
            db.session.commit()
            estado=True
            mensaje="Genero Eliminado Correctamente"            
        else:
            mensaje="Tarea no permitida"
    except exc.SQLAlchemyError as error:
        db.session.rollback()
        mensaje=str(error)
        
    return {"estado": estado, "mensaje":mensaje}
    