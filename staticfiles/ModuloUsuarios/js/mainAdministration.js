function EditarUsuario(id) {
    window.location.href = "../CrearUsuario/" + id;
}

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
    swal({
        title: "¿Estás seguro?",
        text: "Se modificara el estado del Usuario",
        icon: "warning",
        buttons: {
            confirm: { text: 'Confirmar', className: 'btn-success' },
            cancel: 'Cancelar'
        },
        dangerMode: true,
    }).then((changeStatus) => {
        if (changeStatus) {
            $(document).ready(function() {
                $.ajax({
                    data: { "csrfmiddlewaretoken": token, "estado": ids },
                    url: $("#EstadoUsuarioForm").attr('action'),
                    type: $("#EstadoUsuarioForm").attr('method'),
                    success: function(datas) {
                        swal("¡OK! Se ha modificado el Usuario", {
                            icon: "success",
                        }).then(function() {
                            location.reload()
                        });
                    },
                    error: function(error) {
                        console.log("no")
                        alert("Error:" + error.responseJSON)
                    }
                });
            })
        } else {
            swal("¡OK! Ningún dato del usuario ha sido modificado").then(function() {
                location.reload()
            });

        }
    });
}

function redirect(url) {
    window.location.href = url;
}