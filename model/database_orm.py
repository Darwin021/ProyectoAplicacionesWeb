from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Declarative base for all models
Base = declarative_base()

class Database_ORM:
    def __init__(self, db_url="mysql+pymysql://root:DZGamer02!@localhost:3306/ticketturno"):
        self.db_url = db_url
        self.engine = create_engine(self.db_url, echo=True)
        self.Session = sessionmaker(bind=self.engine)
        self.session = None

    def connect(self):
        """Crea una nueva sesión de base de datos."""
        try:
            self.session = self.Session()
            print("✅ Conexión ORM exitosa")
        except Exception as e:
            print(f"❌ Error al conectar con la base de datos ORM: {e}")
            self.session = None

    def create_all(self):
        """Crea todas las tablas en la base de datos."""
        try:
            Base.metadata.create_all(self.engine)
            print("✅ Tablas creadas (si no existen)")
        except Exception as e:
            print(f"❌ Error al crear las tablas: {e}")

    def commit(self):
        """Confirma los cambios en la base de datos."""
        if self.session:
            try:
                self.session.commit()
                print("✅ Cambios confirmados")
            except Exception as e:
                print(f"❌ Error al confirmar cambios: {e}")
                self.session.rollback()

    def query(self, model):
        """Realiza una consulta a la base de datos para un modelo específico."""
        if self.session:
            try:
                return self.session.query(model)
            except Exception as e:
                print(f"❌ Error en la consulta: {e}")
                return None
        else:
            print("❌ Conexión no disponible")
            return None

    def close(self):
        """Cierra la sesión de la base de datos."""
        if self.session:
            try:
                self.session.close()
                print("🔌 Conexión ORM cerrada")
            except Exception as e:
                print(f"❌ Error al cerrar la sesión: {e}")
        else:
            print("❌ No hay sesión para cerrar.")

# Exportar engine y Session para uso externo
db_orm = Database_ORM()
engine = db_orm.engine
Session = db_orm.Session
