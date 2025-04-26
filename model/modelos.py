from sqlalchemy import Column, String, Integer, ForeignKey, TIMESTAMP, BLOB
from sqlalchemy.orm import relationship
from model.database_orm import Base

class Usuarios(Base):
    __tablename__ = 'Usuarios'
    CURP = Column(String(18), primary_key=True)
    Nombre = Column(String(50), nullable=False)
    Paterno = Column(String(50), nullable=False)
    Materno = Column(String(50), nullable=False)
    Telefono = Column(String(15))
    Celular = Column(String(15))
    Correo = Column(String(100))

    tickets = relationship('Tickets', back_populates='usuario')

class Niveles(Base):
    __tablename__ = 'Niveles'
    NivelID = Column(Integer, primary_key=True, autoincrement=True)
    NombreNivel = Column(String(50), unique=True, nullable=False)

class Municipios(Base):
    __tablename__ = 'Municipios'
    MunicipioID = Column(Integer, primary_key=True, autoincrement=True)
    NombreMunicipio = Column(String(100), unique=True, nullable=False)

class Asuntos(Base):
    __tablename__ = 'Asuntos'
    AsuntoID = Column(Integer, primary_key=True, autoincrement=True)
    NombreAsunto = Column(String(100), unique=True, nullable=False)

class Tickets(Base):
    __tablename__ = 'Tickets'
    TicketID = Column(Integer, primary_key=True, autoincrement=True)
    CURP = Column(String(18), ForeignKey('Usuarios.CURP'))
    Turno = Column(Integer)
    Estatus = Column(String(18))
    NivelID = Column(Integer, ForeignKey('Niveles.NivelID'))
    MunicipioID = Column(Integer, ForeignKey('Municipios.MunicipioID'))
    AsuntoID = Column(Integer, ForeignKey('Asuntos.AsuntoID'))
    FechaCreacion = Column(TIMESTAMP)

    usuario = relationship('Usuarios', back_populates='tickets')
    nivel = relationship('Niveles')
    municipio = relationship('Municipios')
    asunto = relationship('Asuntos')
    qr = relationship('CodigosQR', uselist=False, back_populates='ticket')

class CodigosQR(Base):
    __tablename__ = 'CodigosQR'
    QRID = Column(Integer, primary_key=True, autoincrement=True)
    TicketID = Column(Integer, ForeignKey('Tickets.TicketID'))
    QRCode = Column(BLOB)

    ticket = relationship('Tickets', back_populates='qr')

class Admins(Base):
    __tablename__ = 'Admins'
    Usuario = Column(String(100), primary_key=True)
    contrasena = Column(String(100), unique=True, nullable=False)