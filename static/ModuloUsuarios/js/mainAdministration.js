function añadirUsuario() {
    window.location.href = "../CrearUsuario/";
}

function cancelCreate() {
    window.location.href = "../Administracion/";
}
const getValueInput = () => {
    let inputValue = document.getElementById("Idate").value;
    document.getElementById("valueInput").innerHTML = inputValue;
}

function CambiarEstadoUsuario(id) {
    let ids = id
    let token = $("#EstadoUsuarioForm").find('input[name=csrfmiddlewaretoken]').val()
    console.log(token)
    swal({
        title: "Estas seguro?",
        text: "Se modificara el estado del Usuario",
        icon: "warning",
        buttons: true,
        dangerMode: true,
    }).then((changeStatus) => {
        if (changeStatus) {
            $(document).ready(function() {
                $.ajax({
                    data: { "csrfmiddlewaretoken": token, "estado": ids },
                    url: $("#EstadoUsuarioForm").attr('action'),
                    type: $("#EstadoUsuarioForm").attr('method'),
                    success: function(data) {
                        window.location.href = "/InformacionUsuario/Administracion/"
                    },
                    error: function(error) {
                        console.log("no")
                        alert("Error:" + error.responseJSON)
                    }
                });
            })
        } else {
            swal("OK! Ningun dato del servicio ha sido modificado").then(function() {
                location.reload()
            });

        }
    });

}