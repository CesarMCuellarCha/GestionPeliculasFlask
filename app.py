from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

user,password,host,database = "root","adsocauca","localhost","gestionpeliculas"

cadenaConexion = f"mysql+pymysql://{user}:{password}@{host}/{database}"

cadenaConexionSqlite = "sqlite:///gestionPeliculas.db"

app.config['SQLALCHEMY_DATABASE_URI']=cadenaConexionSqlite

db = SQLAlchemy(app)

if __name__=="__main__":
    from routes.genero import *
    from routes.pelicula import *
    
    #crea las tablas de acuerdo con los modelos
    with app.app_context():
        db.create_all()
        
    app.run(port=5400, debug=True)
    
    