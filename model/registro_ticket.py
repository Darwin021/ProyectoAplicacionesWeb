import os
import io
import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import joinedload
from model.database_orm import engine, Session
from model.modelos import Usuarios, Tickets, CodigosQR, Municipios, Niveles,Asuntos
from datetime import datetime

Session = sessionmaker(bind=engine)

def registrar_ticket(datos_usuario, datos_ticket):
    session = Session()
    try:
        curp = datos_usuario['CURP']
        usuario = session.query(Usuarios).filter_by(CURP=curp).first()
        if not usuario:
            usuario = Usuarios(
                CURP=curp,
                Nombre=datos_usuario['Nombre'],
                Paterno=datos_usuario['Paterno'],
                Materno=datos_usuario['Materno'],
                Telefono=datos_usuario['Telefono'],
                Celular=datos_usuario['Celular'],
                Correo=datos_usuario['Correo']
            )
            session.add(usuario)

        # Obtener el municipio y nivel usando los IDs proporcionados
        municipio = session.query(Municipios).filter_by(MunicipioID=datos_ticket['MunicipioID']).first()
        nivel = session.query(Niveles).filter_by(NivelID=datos_ticket['NivelID']).first()

        # Contar el número de tickets existentes para el municipio y asignar el turno
        turno = session.query(Tickets).filter_by(MunicipioID=datos_ticket['MunicipioID']).count() + 1

        nuevo_ticket = Tickets(
            CURP=curp,
            Estatus="Pendiente",
            NivelID=datos_ticket['NivelID'],
            MunicipioID=datos_ticket['MunicipioID'],
            AsuntoID=datos_ticket['AsuntoID'],
            FechaCreacion=datetime.now(),  # Asegúrate de registrar la fecha de creación
            Turno=turno  # Asignar el turno calculado
        )
        session.add(nuevo_ticket)
        session.commit()

        ticket_id = nuevo_ticket.TicketID
        session.commit()

        # Crear el código QR con la CURP
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(curp)  # Generamos el QR con la CURP
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        qr_filename = f"qr_{ticket_id}.png"
        qr_path = os.path.join("static/qr_codes", qr_filename)
        os.makedirs(os.path.dirname(qr_path), exist_ok=True)
        img.save(qr_path)

        # Guardamos el código QR como un objeto CodigosQR
        with open(qr_path, 'rb') as f:
            qr_blob = f.read()

        nuevo_qr = CodigosQR(TicketID=ticket_id, QRCode=qr_blob)
        session.add(nuevo_qr)
        session.commit()

        # Generar el PDF en memoria
        pdf_buffer = io.BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=letter)
        c.drawString(100, 750, "Comprobante de Registro")
        c.drawString(100, 730, f"Turno: {turno}")  # Mostrar el turno correcto
        c.drawString(100, 710, f"Nombre: {datos_usuario['Nombre']} {datos_usuario['Paterno']} {datos_usuario['Materno']}")
        c.drawString(100, 690, f"Municipio: {municipio.NombreMunicipio}")  # Nombre del municipio
        c.drawString(100, 670, f"Nivel: {nivel.NombreNivel}")  # Nombre del nivel
        c.drawImage(qr_path, 100, 500, width=150, height=150)
        c.save()
        pdf_buffer.seek(0)

        return f"✅ Ticket registrado correctamente con turno {turno}", pdf_buffer, ticket_id

    except Exception as e:
        session.rollback()
        print(f"Error al registrar ticket: {e}")
        raise e
    finally:  
        session.close()