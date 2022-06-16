$(document).ready(function() {
    let permiso = document.querySelectorAll('#PermisoName')
    
    for (let i = 0; i < permiso.length; i++) {
        name = permiso[i].innerHTML
        name = name.replace("Can", "Puede")
        name = name.replace("delete","eliminar")
        name = name.replace("view","ver")
        name = name.replace("add","añadir")
        name = name.replace("change","modificar")
        name = name.replace("log entry","iniciar sesión")
        name = name.replace("group","roles")
        name = name.replace("permission","permisos")
        name = name.replace("notificacion","notificación")
        name = name.replace("content type","tipo de contenido")
        name = name.replace("codigo postal","código postal")
        permiso[i].innerHTML = name
    }
    let permiso2 = document.querySelectorAll('#PermisoNameA')
    for (let i = 0; i < permiso2.length; i++) {
        name = permiso2[i].innerHTML
        name = name.replace("Can", "Puede")
        name = name.replace("delete","eliminar")
        name = name.replace("view","ver")
        name = name.replace("add","añadir")
        name = name.replace("change","modificar")
        name = name.replace("log entry","iniciar sesión")
        name = name.replace("group","roles")
        name = name.replace("permission","permisos")
        name = name.replace("notificacion","notificación")
        name = name.replace("content type","tipo de contenido")
        name = name.replace("codigo postal","código postal")
        permiso2[i].innerHTML = name
    }
});