from flask import request
from app import app, db
from models.pelicula import *
from models.genero import *
from sqlalchemy import exc

@app.route("/pelicula/", methods=['GET'])
def listar():
    try:
        mensaje=None
        listaPeliculas=[]
        if request.method=='GET':
            peliculas = Pelicula.query.all()
            for p in peliculas:
                pelicula={
                    "id": p.idPelicula,
                    "codigo":p.pelCodigo,
                    "titulo":p.pelTitulo,
                    "protagonista": p.pelProtagonista,
                    "duracion": p.pelDuracion,
                    "foto": p.pelFoto,
                    "genero":{
                        "id": p.genero.idGenero,
                        "nombre": p.genero.genNombre
                    }
                }
                listaPeliculas.append(pelicula)
        else:
            mensaje="Tarea no permitida"        
    except exc.SQLAlchemyError as error:
        mensaje=str(error)
        
    return {"mensaje":mensaje, "peliculas": listaPeliculas}

@app.route("/pelicula/", methods=['POST'])
def addPelicula():
    try:
        estado=False
        mensaje=None
        if request.method=='POST':
            datos=request.get_json(force=True)
            genero = Genero.query.get(int(datos['genero']))
            pelicula=Pelicula(pelCodigo = int(datos['codigo']),
                              pelTitulo=datos['titulo'],
                              pelProtagonista=datos['protagonista'],
                              pelDuracion=datos['duracion'],
                              pelResumen=datos['resumen'],
                              pelFoto=f"{int(datos['codigo'])}.jpg",
                              genero = genero)
            
            db.session.add(pelicula)
            db.session.commit()
            estado=True
            mensaje=f"Pelicula Agregada correctamente con ID: {pelicula.idPelicula}"
        else:
            mensaje="Tarea no permitida"
    except exc.SQLAlchemyError as error:
        db.session.rollback()
        mensaje=str(error)
        
    return {"estado": estado, "mensaje": mensaje}