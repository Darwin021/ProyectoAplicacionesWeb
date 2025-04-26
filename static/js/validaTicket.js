var pattern_curp = /^[A-Z]{4}\d{6}[HM]{1}[A-Z]{2}[B-DF-HJ-NP-TV-Z]{3}[A-Z\d]{1}\d{1}$/;
var pattern_nombre = /^[A-Za-zÁÉÍÓÚáéíóúüÜñÑ\s]+$/;
var pattern_telefono = /^[0-9]{10}$/;
var pattern_celular = /^[0-9]{10}$/;
var pattern_email=/^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}?$/;

let mensaje = (tipo,titulo,texto,liga) => {
    Swal.fire({
        title: titulo,
        text: texto,
        icon: tipo,
        footer: liga
    });
}

let validaTicket = () => {
    let js_nombre = document.getElementById('nombre_completo').value;
    let js_curp = document.getElementById('curp').value;
    let js_nombres = document.getElementById('nombres').value;
    let js_paterno = document.getElementById('paterno').value;
    let js_materno = document.getElementById('materno').value;
    let js_telefono = document.getElementById('telefono').value;
    let js_celular = document.getElementById('celular').value;
    let js_email = document.getElementById('correo').value;
    let js_nivel = document.getElementById('nivel').value;
    let js_municipio = document.getElementById('municipio').value;
    let js_asunto = document.getElementById('asunto').value;

    if (js_nombre.length == 0) {
        mensaje('warning', '¡Atención!', 'Debes ingresar tu nombre completo', '');
        return false;
    }
    if (!pattern_nombre.test(js_nombre)) {
        mensaje('error', '¡Error!', 'El nombre ingresado no es válido', '');
        return false;
    }
    if (js_curp.length == 0) {
        mensaje('warning', '¡Atención!', 'Debes ingresar tu CURP', '<a href="https://www.gob.mx/curp/" target="_blank"> Consulte su CURP?</a>');
        return false;
    }
    if (!pattern_curp.test(js_curp)) {
        mensaje('error', '¡Error!', 'El CURP ingresado no es válido', '<a href="https://www.gob.mx/curp/" target="_blank"> Consulte su CURP?</a>');
        return false;
    }
    if (js_nombres.length == 0 || js_paterno.length == 0 || js_materno.length == 0) {
        mensaje('error', '¡Error!', 'Los campos nombre, paterno y materno son obligatorios', '');
        return false;
    }
    if (js_telefono.length == 0 || !pattern_telefono.test(js_telefono)) {
        mensaje('error', '¡Error!', 'El teléfono ingresado no es válido', '');
        return false;
    }
    if (js_celular.length == 0 || !pattern_celular.test(js_celular)) {   
        mensaje('error', '¡Error!', 'El celular ingresado no es válido', '');
        return false;
    }
    if (js_email.length == 0 || !pattern_email.test(js_email)) {
        mensaje('error', '¡Error!', 'El email ingresado no es válido', '');
        return false;
    }
    if (js_nivel == 0) {
        mensaje('error', '¡Error!', 'Debe seleccionar un nivel', '');
        return false;
    }
    if (js_municipio == 0) {
        mensaje('error', '¡Error!', 'Debe seleccionar un municipio', '');
        return false;
    }
    if (js_asunto == 0) {
        mensaje('error', '¡Error!', 'El campo asunto es obligatorio', '');
        return false;
    }

    // 🆕 Mostrar mensaje de éxito antes de enviar el formulario
    Swal.fire({
        title: '¡Registro exitoso!',
        text: 'Los datos han sido guardados correctamente',
        icon: 'success'
    }).then(() => {
        document.forms["registro"].submit();  // Enviar formulario después de la alerta
        limpiarFormulario();  // Limpiar formulario después del envío
    });

    return false; // Para evitar el envío automático
}

function limpiarFormulario() {
    // Limpiar los campos del formulario
    document.getElementById('nombre_completo').value = "";
    document.getElementById('curp').value = "";
    document.getElementById('nombres').value = "";
    document.getElementById('paterno').value = "";
    document.getElementById('materno').value = "";
    document.getElementById('telefono').value = "";
    document.getElementById('celular').value = "";
    document.getElementById('correo').value = "";
    document.getElementById('nivel').selectedIndex = 0;
    document.getElementById('municipio').selectedIndex = 0;
    document.getElementById('asunto').selectedIndex = 0;
    
    // Limpiar el QR y ocultarlo
    let qrImage = document.getElementById("qrImage");
    qrImage.src = "";  // Borrar la URL del QR
    qrImage.style.display = "none";  // Ocultar el QR
}

