from model.database_orm import Database_ORM
from model.modelos import Usuarios, Tickets, CodigosQR, Niveles, Municipios, Asuntos
from sqlalchemy.orm import joinedload,Session

class AdminCRUD:
    def __init__(self):
        self.db = Database_ORM()
        self.db.connect()

    def obtener_tickets_completos(self):
        try:
            tickets = (
                self.db.session.query(Tickets)
                .options(
                    joinedload(Tickets.usuario),
                    joinedload(Tickets.nivel),
                    joinedload(Tickets.municipio),
                    joinedload(Tickets.asunto),
                    joinedload(Tickets.qr)
                )
                .all()
            )

            datos = []
            for ticket in tickets:
                datos.append({
                    'Turno': ticket.Turno,
                    'Tutor': ticket.CURP,
                    'CURP': ticket.CURP,
                    'NombreCompleto': f"{ticket.usuario.Nombre} {ticket.usuario.Paterno} {ticket.usuario.Materno}",
                    'Celular': ticket.usuario.Celular,
                    'Correo': ticket.usuario.Correo,
                    'Nivel': ticket.nivel.NombreNivel,
                    'Municipio': ticket.municipio.NombreMunicipio,
                    'Asunto': ticket.asunto.NombreAsunto,
                    'QRCode': ticket.qr.QRCode if ticket.qr else None,
                    'Estatus': ticket.Estatus,
                    'FechaCreacion': ticket.FechaCreacion.strftime('%Y-%m-%d %H:%M:%S') if ticket.FechaCreacion else ''
                })
            return datos
        except Exception as e:
            print(f"❌ Error al obtener tickets: {e}")
            return []

    def modificar_ticket_por_id(self, ticket_id, datos_usuario, datos_ticket):
        try:
            ticket = (
                self.db.session.query(Tickets)
                .options(joinedload(Tickets.usuario))
                .filter(Tickets.TicketID == ticket_id)
                .first()
            )

            if not ticket:
                raise Exception("Ticket no encontrado")

            if ticket.usuario:
                ticket.usuario.Nombre = datos_usuario.get('Nombre', ticket.usuario.Nombre)
                ticket.usuario.Paterno = datos_usuario.get('Paterno', ticket.usuario.Paterno)
                ticket.usuario.Materno = datos_usuario.get('Materno', ticket.usuario.Materno)
                ticket.usuario.Telefono = datos_usuario.get('Telefono', ticket.usuario.Telefono)
                ticket.usuario.Celular = datos_usuario.get('Celular', ticket.usuario.Celular)
                ticket.usuario.Correo = datos_usuario.get('Correo', ticket.usuario.Correo)

            ticket.Estatus = datos_ticket.get('Estatus', ticket.Estatus)
            ticket.NivelID = datos_ticket.get('NivelID', ticket.NivelID)
            ticket.MunicipioID = datos_ticket.get('MunicipioID', ticket.MunicipioID)
            ticket.AsuntoID = datos_ticket.get('AsuntoID', ticket.AsuntoID)

            self.db.session.commit()
            print(f"✅ Ticket actualizado correctamente para TicketID={ticket_id}")
            return True

        except Exception as e:
            print(f"❌ Error al modificar el ticket: {e}")
            self.db.session.rollback()
            return False

    def obtener_ticket_por_id(self, ticket_id):
        try:
            return (
                self.db.session.query(Tickets)
                .options(joinedload(Tickets.usuario))
                .filter(Tickets.TicketID == ticket_id)
                .first()
            )
        except Exception as e:
            print(f"❌ Error al obtener ticket por ID: {e}")
            return None

    def eliminar_ticket_por_id(self, ticket_id):
        try:
            ticket = (
                self.db.session.query(Tickets)
                .options(joinedload(Tickets.qr), joinedload(Tickets.usuario))
                .filter(Tickets.TicketID == ticket_id)
                .first()
            )

            if not ticket:
                raise Exception("Ticket no encontrado")

            if ticket.qr:
                self.db.session.delete(ticket.qr)

            if ticket.usuario:
                self.db.session.delete(ticket.usuario)

            self.db.session.delete(ticket)
            self.db.session.commit()
            print(f"✅ Ticket, usuario y código QR eliminados correctamente para TicketID={ticket_id}")
            return True

        except Exception as e:
            print(f"❌ Error al eliminar el ticket, usuario o código QR: {e}")
            self.db.session.rollback()
            return False
        
    def obtener_ticket_por_curp_y_turno(self, curp, turno):
        try:
            ticket = (
                self.db.session.query(Tickets)
                .options(joinedload(Tickets.usuario))
                .filter(Tickets.CURP == curp, Tickets.Turno == turno)
                .first()
            )
            return ticket
        except Exception as e:
            print(f"❌ Error al obtener ticket por CURP y Turno: {e}")
            return None

    def buscar_tickets(self, query):
        try:
            query_lower = f"%{query.lower()}%"
            tickets = (
                self.db.session.query(Tickets)
                .join(Tickets.usuario)
                .join(Tickets.nivel)
                .join(Tickets.municipio)
                .join(Tickets.asunto)
                .outerjoin(Tickets.qr)
                .filter(
                    (Usuarios.CURP.ilike(query_lower)) |
                    (Usuarios.Nombre.ilike(query_lower)) |
                    (Usuarios.Paterno.ilike(query_lower)) |
                    (Usuarios.Materno.ilike(query_lower))
                )
                .all()
            )

            datos = []
            for ticket in tickets:
                datos.append({
                    'Turno': ticket.Turno,
                    'Tutor': ticket.CURP,
                    'CURP': ticket.CURP,
                    'NombreCompleto': f"{ticket.usuario.Nombre} {ticket.usuario.Paterno} {ticket.usuario.Materno}",
                    'Celular': ticket.usuario.Celular,
                    'Correo': ticket.usuario.Correo,
                    'Nivel': ticket.nivel.NombreNivel,
                    'Municipio': ticket.municipio.NombreMunicipio,
                    'Asunto': ticket.asunto.NombreAsunto,
                    'QRCode': ticket.qr.QRCode if ticket.qr else None,
                    'Estatus': ticket.Estatus,
                    'FechaCreacion': ticket.FechaCreacion.strftime('%Y-%m-%d %H:%M:%S') if ticket.FechaCreacion else ''
                })
            return datos
        except Exception as e:
            print(f"❌ Error al buscar tickets: {e}")
            return []

