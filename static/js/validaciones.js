// Validaciones con expresiones regulares
const pattern_nombre = /^[A-Za-zÁÉÍÓÚáéíóúüÜñÑ\s]+$/;
const pattern_telefono = /^[0-9]{10}$/;
const pattern_celular = /^[0-9]{10}$/;
const pattern_email = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}?$/;

const mensaje = (tipo, titulo, texto, liga) => {
    Swal.fire({
        title: titulo,
        text: texto,
        icon: tipo,
        footer: liga
    });
};

const validarModificacion = () => {
    const nombres = document.getElementById('nombre').value.trim();
    const paterno = document.getElementById('paterno').value.trim();
    const materno = document.getElementById('materno').value.trim();
    const telefono = document.getElementById('telefono').value.trim();
    const celular = document.getElementById('celular').value.trim();
    const correo = document.getElementById('correo').value.trim();
    const tutor = document.getElementById('tutor').value.trim();
    const nivel = document.getElementById('nivel').value;
    const municipio = document.getElementById('municipio').value;
    const asunto = document.getElementById('asunto').value;

    if (!nombres || !paterno || !materno) {
        mensaje('warning', '¡Atención!', 'Todos los campos de nombre son obligatorios', '');
        return false;
    }

    if (!pattern_nombre.test(nombres) || !pattern_nombre.test(paterno) || !pattern_nombre.test(materno)) {
        mensaje('error', '¡Error!', 'Nombre(s) y apellidos deben contener solo letras', '');
        return false;
    }

    if (!telefono || !pattern_telefono.test(telefono)) {
        mensaje('error', '¡Error!', 'El teléfono debe tener 10 dígitos numéricos', '');
        return false;
    }

    if (!celular || !pattern_celular.test(celular)) {
        mensaje('error', '¡Error!', 'El celular debe tener 10 dígitos numéricos', '');
        return false;
    }

    if (!correo || !pattern_email.test(correo)) {
        mensaje('error', '¡Error!', 'Correo electrónico inválido', '');
        return false;
    }

    if (!tutor || !pattern_nombre.test(tutor)) {
        mensaje('error', '¡Error!', 'El nombre del tutor es obligatorio y debe ser válido', '');
        return false;
    }

    if (nivel == "0") {
        mensaje('warning', '¡Atención!', 'Debe seleccionar un nivel', '');
        return false;
    }

    if (municipio == "0") {
        mensaje('warning', '¡Atención!', 'Debe seleccionar un municipio', '');
        return false;
    }

    if (asunto == "0") {
        mensaje('warning', '¡Atención!', 'Debe seleccionar un asunto', '');
        return false;
    }

    // Confirmación
    Swal.fire({
        title: '¿Guardar cambios?',
        text: 'Estás a punto de actualizar este ticket',
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Sí, guardar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            document.getElementById('formulario').submit();
        }
    });

    return false;
};

window.onload = () => {
    document.getElementById('formulario').addEventListener('submit', function (e) {
        e.preventDefault();
        validarModificacion();
    });
};

