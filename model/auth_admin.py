from model.database_orm import Session
from model.modelos import Admins

def validar_admin(usuario, contrasena):
    session = Session()
    try:
        # Buscar al administrador con el usuario y la contraseña proporcionados
        admin = session.query(Admins).filter_by(Usuario=usuario, contrasena=contrasena).first()
        return bool(admin)
    finally:
        session.close()
