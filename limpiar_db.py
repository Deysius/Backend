from flask import Flask
from database import db

# Importamos todos los modelos para asegurar que Flask los reconozca
from models.usuario import Usuario
from models.rol import Rol
from models.meta import Meta
from models.proyecto import Proyecto
from models.avance_proyecto import AvanceProyecto
from models.registro_actividad import RegistroActividad
from models.historico_productividad import HistoricoProductividad
from models.plan_mejora import PlanMejora
from models.rol_aplicacion import RolAplicacion
from models.aplicacion import Aplicacion

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///timewise.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def purgar_tablas():
    with app.app_context():
        print("⏳ Iniciando purga selectiva de la base de datos...")
        
        try:
            # 1. Desactivar temporalmente las restricciones de llave foránea en SQLite
            db.session.execute(db.text("PRAGMA foreign_keys = OFF;"))
            
            # 2. Eliminar los datos de las tablas analíticas y operativas
            # NOTA: No tocamos las tablas 'usuario' ni 'rol'
            db.session.query(PlanMejora).delete()
            db.session.query(HistoricoProductividad).delete()
            db.session.query(RegistroActividad).delete()
            db.session.query(AvanceProyecto).delete()
            db.session.query(Proyecto).delete()
            db.session.query(Meta).delete()
            db.session.query(RolAplicacion).delete()
            db.session.query(Aplicacion).delete()
            
            # Guardar los cambios permanentemente
            db.session.commit()
            
            # 3. Reactivar la verificación de llaves foráneas
            db.session.execute(db.text("PRAGMA foreign_keys = ON;"))
            
            print("✅ ¡Limpieza exitosa! Las tablas analíticas y de proyectos están vacías.")
            print("👤 Tus usuarios y roles se mantuvieron intactos.")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error al limpiar la base de datos: {str(e)}")

if __name__ == "__main__":
    purgar_tablas()