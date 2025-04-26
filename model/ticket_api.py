from flask import Blueprint, request, jsonify
from model.database_orm import Database_ORM
from model.modelos import Tickets, Usuarios, Niveles, Municipios, Asuntos

ticket_api = Blueprint('ticket_api', __name__)

@ticket_api.route('/api/consultar_ticket', methods=['POST'])
def consultar_ticket():
    data = request.get_json()
    curp = data.get('curp')
    turno = data.get('turno')

    if not curp or not turno:
        return jsonify({'error': 'Faltan parámetros'}), 400

    db = Database_ORM()
    db.connect()

    ticket = db.session.query(Tickets).join(Usuarios).filter(
        Tickets.CURP == curp,
        Tickets.Turno == turno
    ).first()

    if not ticket:
        db.close()
        return jsonify({'error': 'No se encontró el ticket'}), 404

    usuario = ticket.usuario
    nivel = ticket.nivel
    municipio = ticket.municipio
    asunto = ticket.asunto

    resultado = {
        'turno': ticket.Turno,
        'estatus': ticket.Estatus,
        'curp': usuario.CURP,
        'nombre': usuario.Nombre,
        'paterno': usuario.Paterno,
        'materno': usuario.Materno,
        'telefono': usuario.Telefono,
        'celular': usuario.Celular,
        'correo': usuario.Correo,
        'nivel': nivel.NombreNivel,
        'municipio': municipio.NombreMunicipio,
        'asunto': asunto.NombreAsunto,
        'fecha': ticket.FechaCreacion.strftime('%Y-%m-%d %H:%M:%S')
    }

    db.close()
    return jsonify(resultado)