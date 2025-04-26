from model.database_orm import Session
from model.modelos import Niveles, Municipios, Asuntos
import re

def validar_telefono(telefono):
    return bool(re.match(r'^\d{10}$', telefono))

def validar_correo(correo):
    return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', correo))

def validar_nivel(nivel_id):
    session = Session()
    try:
        # Verificar si existe un nivel con el ID proporcionado
        nivel = session.query(Niveles).filter_by(NivelID=nivel_id).first()
        return bool(nivel)
    finally:
        session.close()

def validar_municipio(municipio_id):
    session = Session()
    try:
        # Verificar si existe un municipio con el ID proporcionado
        municipio = session.query(Municipios).filter_by(MunicipioID=municipio_id).first()
        return bool(municipio)
    finally:
        session.close()

def validar_asunto(asunto_id):
    session = Session()
    try:
        # Verificar si existe un asunto con el ID proporcionado
        asunto = session.query(Asuntos).filter_by(AsuntoID=asunto_id).first()
        return bool(asunto)
    finally:
        session.close()

