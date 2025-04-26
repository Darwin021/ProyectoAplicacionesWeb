import os
import json
import requests
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, session, jsonify
from model.database_orm import Database_ORM
from model.auth_admin import validar_admin
from model.registro_ticket import registrar_ticket
from model.CRUD_admin import AdminCRUD
from model.modelos import Tickets, Niveles, Municipios, Asuntos, Usuarios

app = Flask(__name__)
app.secret_key = "super_secret_key"

# Ruta para la carpeta "Descargas"
DOWNLOADS_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")
if not os.path.exists(DOWNLOADS_FOLDER):
    os.makedirs(DOWNLOADS_FOLDER)

# Página de login del administrador
@app.route('/login-admin')
def mostrar_login_admin():
    return render_template('login-admin.html')

@app.route("/admin-login", methods=["POST"])
def admin_login():
    usuario = request.form["username"]
    contrasena = request.form["password"]
    recaptcha_response = request.form.get("g-recaptcha-response")

    # Verifica el captcha con Google
    secret_key = "6LcrigorAAAAANfoaP5jtN61hKtrwXW_1djvtj7W"
    captcha_verify_url = "https://www.google.com/recaptcha/api/siteverify"
    payload = {
        "secret": secret_key,
        "response": recaptcha_response
    }
    response = requests.post(captcha_verify_url, data=payload)
    result = response.json()

    if not result.get("success"):
        flash("❌ Verificación de CAPTCHA fallida", "error")
        return redirect(url_for("mostrar_login_admin"))

    if validar_admin(usuario, contrasena):
        session["admin"] = usuario
        return redirect(url_for("Mostrar_tickets"))
    else:
        flash("❌ Usuario o contraseña incorrectos", "error")
        return redirect(url_for("mostrar_login_admin"))

@app.route("/admin", methods=["GET"])
def Mostrar_tickets():
    if "admin" not in session:
        return redirect(url_for("mostrar_login_admin"))
    
    admin_crud = AdminCRUD()
    tickets = admin_crud.obtener_tickets_completos()
    admin_crud.db.session.close()
    return render_template("admins.html", tickets=tickets)

@app.route("/buscar", methods=["GET"])
def buscar_tickets():
    if "admin" not in session:
        return redirect(url_for("mostrar_login_admin"))

    query = request.args.get("query", "").strip()
    admin_crud = AdminCRUD()

    if query:
        tickets = admin_crud.buscar_tickets(query)
    else:
        tickets = admin_crud.obtener_tickets_completos()

    return render_template("admins.html", tickets=tickets)

@app.route("/", methods=["GET", "POST"])
def add_aspirante():
    if request.method == "POST":
        datos_usuario = {
            'CURP': request.form['curp'],
            'Nombre': request.form['nombres'],
            'Paterno': request.form['paterno'],
            'Materno': request.form['materno'],
            'Telefono': request.form['telefono'],
            'Celular': request.form['celular'],
            'Correo': request.form['correo']
        }

        datos_ticket = {
            'NivelID': request.form['nivel'],
            'MunicipioID': request.form['municipio'],
            'AsuntoID': request.form['asunto']
        }

        tutor = request.form['nombre_completo']

        if not all([*datos_usuario.values(), *datos_ticket.values(), tutor]):
            flash("Por favor, complete todos los campos", "danger")
            return redirect(url_for("add_aspirante"))

        try:
            mensaje, pdf_buffer, curp = registrar_ticket(datos_usuario, datos_ticket)

            if pdf_buffer:
                pdf_filename = os.path.join(DOWNLOADS_FOLDER, f"comprobante_turno_{datos_usuario['CURP']}.pdf")
                with open(pdf_filename, 'wb') as f:
                    f.write(pdf_buffer.getvalue())
                session['pdf_filename'] = pdf_filename
                flash(mensaje, "success" if "Ticket registrado" in mensaje else "danger")
                return redirect(url_for("descargar_pdf"))
            else:
                flash("❌ No se pudo generar el PDF", "error")
        except Exception as e:
            flash(f"❌ Error al registrar el ticket: {str(e)}", "error")
            return redirect(url_for("add_aspirante"))

    return render_template("ticket.html")

@app.route('/eliminar-ticket/<int:ticket_id>', methods=['POST'])
def eliminar_ticket(ticket_id):
    try:
        admin_crud = AdminCRUD()
        admin_crud.eliminar_ticket_por_id(ticket_id)
        admin_crud.db.session.close()
        flash("✅ Ticket eliminado correctamente", "success")
    except Exception as e:
        flash(f"❌ Error al eliminar el ticket: {str(e)}", "error")
    
    return redirect(url_for('Mostrar_tickets'))

@app.route("/modificar_ticket/<int:ticket_id>", methods=["GET", "POST"])
def modificar_ticket(ticket_id):
    if "admin" not in session:
        return redirect(url_for("mostrar_login_admin"))
    
    admin_crud = AdminCRUD()
    ticket = admin_crud.obtener_ticket_por_id(ticket_id)

    if not ticket:
        flash("❌ Ticket no encontrado", "error")
        return redirect(url_for("Mostrar_tickets"))

    niveles = admin_crud.db.session.query(Niveles).all()
    municipios = admin_crud.db.session.query(Municipios).all()
    asuntos = admin_crud.db.session.query(Asuntos).all()

    if request.method == "POST":
        datos_usuario = {
            'Nombre': request.form['Nombre'],
            'Paterno': request.form['Paterno'],
            'Materno': request.form['Materno'],
            'Telefono': request.form['Telefono'],
            'Celular': request.form['Celular'],
            'Correo': request.form['Correo']
        }

        datos_ticket = {
            'Estatus': request.form['Estatus'],
            'NivelID': request.form['NivelID'],
            'MunicipioID': request.form['MunicipioID'],
            'AsuntoID': request.form['AsuntoID']
        }

        success = admin_crud.modificar_ticket_por_id(ticket_id, datos_usuario, datos_ticket)

        if success:
            flash("✅ Ticket actualizado correctamente", "success")
            return redirect(url_for("Mostrar_tickets"))
        else:
            flash("❌ Error al actualizar el ticket", "error")

    return render_template("modificar_ticket.html", ticket=ticket, niveles=niveles, municipios=municipios, asuntos=asuntos)

@app.route("/descargar-pdf")
def descargar_pdf():
    if "pdf_filename" in session:
        pdf_filename = session.pop("pdf_filename")
        return send_from_directory(DOWNLOADS_FOLDER, os.path.basename(pdf_filename), as_attachment=True)
    else:
        flash("❌ No se pudo generar el PDF", "error")
        return redirect(url_for("add_aspirante"))

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "admin" not in session:
        return redirect(url_for("mostrar_login_admin"))

    db_orm = Database_ORM()
    db_orm.connect()
    municipios = db_orm.query(Municipios).all()

    selected_municipio = request.args.get("municipio", None)
    if selected_municipio:
        tickets = db_orm.session.query(Tickets).filter(Tickets.MunicipioID == selected_municipio).all()
    else:
        tickets = db_orm.session.query(Tickets).all()

    pendientes = sum(1 for ticket in tickets if ticket.Estatus == 'Pendiente')
    resueltos = sum(1 for ticket in tickets if ticket.Estatus == 'Resuelto')

    labels = ["Pendiente", "Resuelto"]
    counts = [pendientes, resueltos]

    db_orm.close()
    return render_template("dashboard.html", municipios=municipios, labels=json.dumps(labels), counts=json.dumps(counts))

@app.route('/logout')
def logout():
    session.pop('admin', None)
    flash("✅ Has cerrado sesión exitosamente.", "success")
    return redirect(url_for('mostrar_login_admin'))

@app.route("/consultar_ticket", methods=["GET"])
def mostrar_consulta_ticket():
    return render_template("consulta_ticket.html")


@app.route('/api/consultar_ticket', methods=['POST'])
def consultar_ticket():
    data = request.get_json()
    curp = data.get('curp')
    turno = data.get('turno')

    if not curp or not turno:
        return jsonify({'error': 'Faltan parámetros'}), 400

    db_orm = Database_ORM()
    db_orm.connect()
    
    ticket = db_orm.session.query(Tickets).join(Usuarios).filter(
        Tickets.CURP == curp,
        Tickets.Turno == turno
    ).first()

    if not ticket:
        db_orm.close()
        return jsonify({'error': 'No se encontró el ticket'}), 404

    usuario = ticket.usuario
    nivel = ticket.nivel
    municipio = ticket.municipio
    asunto = ticket.asunto

    ticket_info = {
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

    db_orm.close()
    return jsonify(ticket_info)

@app.route("/modificar_ticket_curp", methods=["GET", "POST"])
def modificar_ticket_curp():
    admin_crud = AdminCRUD()
    
    if request.method == "GET":
        curp = request.args.get('curp')
        turno = request.args.get('turno')
        ticket = admin_crud.obtener_ticket_por_curp_y_turno(curp, turno)  # Obtención del ticket por CURP y Turno
        niveles = admin_crud.db.session.query(Niveles).all()
        municipios = admin_crud.db.session.query(Municipios).all()
        asuntos = admin_crud.db.session.query(Asuntos).all()
        return render_template("modificar_ticket_curp.html", ticket=ticket, niveles=niveles, municipios=municipios, asuntos=asuntos)
    
    if request.method == "POST":
        # Obtener los datos del formulario
        datos_usuario = {
            'Nombre': request.form['Nombre'],
            'Paterno': request.form['Paterno'],
            'Materno': request.form['Materno'],
            'Telefono': request.form['Telefono'],
            'Celular': request.form['Celular'],
            'Correo': request.form['Correo'],
        }
        
        datos_ticket = {
            'NivelID': request.form['NivelID'],
            'MunicipioID': request.form['MunicipioID'],
            'AsuntoID': request.form['AsuntoID'],
        }
        
        # Obtener el TicketID desde el formulario
        ticket_id = request.form.get('TicketID')  # Usamos TicketID en lugar de CURP y Turno
        
        # Modificar el ticket usando el TicketID
        if admin_crud.modificar_ticket_por_id(ticket_id, datos_usuario, datos_ticket):
            flash("Ticket modificado con éxito", "success")
            return redirect(url_for("mostrar_consulta_ticket"))
        else:
            flash("Error al modificar el ticket", "error")
    
    return redirect(url_for("mostrar_consulta_ticket"))

if __name__ == "__main__":
    app.run(debug=True)

