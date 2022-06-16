function agregarprod(url) {
    window.location.href = "../crearprod/";
};

function modificarProb(id) {
    window.location.href = "../modificarprod/" + id;

};

function agregarprov(url) {
    $("#agregar_prov").load(url, function() {
        $(this).modal('show')
    })

};

function modificarprov(url) {
    $("#editar_prov").load(url, function() {
        $(this).modal('show')
    })

};

function modificartp(url) {
    $("#modificar_prod").load(url, function() {
        $(this).modal('show')
    })

};

function agregartp(url) {
    $("#agregar_prod").load(url, function() {
        $(this).modal('show')
    })
};

function agregarcompra(url) {
    window.location.href = "../crearcompra/";
};


function mostrarerrores(errors) {
    $('#errores').html("");
    let error = "";
    for (let item in errors.responseJSON.errors) {
        error += '<div class = "alert alert-danger"<strong>' + errors.responseJSON.errors[item] + '</strong></div>';
    }

    $('#errores').append(error)

}


function registrartp() {

    $.ajax({
        data: $("#agregartp").serialize(),
        url: $("#agregartp").attr('action'),
        type: $("#agregartp").attr('method'),
        success: function(response) {
            location.reload();
        },
        error: function(errors) {
            $('#agregartp').find(".text-danger").text("");
            for (let e in errors.responseJSON["errors"]) {
                let campo = $('#agregartp').find("input[name=" + e + "]")
                campo.addClass("is-invalid")
                $('#' + e).text(errors.responseJSON['errors'][e])
            }


        }
    });
}


function registrarcpd() {

    $.ajax({
        data: $("#agregarprod").serialize(),
        url: $("#agregarprod").attr('action'),
        type: $("#agregarprod").attr('method'),
        success: function(response) {
            location.reload();
        },
        error: function(errors) {
            $('#agregarprod').find(".text-danger").text("");
            for (let e in errors.responseJSON["errors"]) {
                let campo = $('#agregarprod').find("input[name=" + e + "]")
                campo.addClass("is-invalid")
                $('#' + e).text(errors.responseJSON['errors'][e])
            }


        }
    });
}

function registrarcomp() {

    $.ajax({
        data: $("#agregarcomp").serialize(),
        url: $("#agregarcomp").attr('action'),
        type: $("#agregarcomp").attr('method'),
        success: function(response) {
            location.reload();
        },
        error: function(errors) {
            $('#agregarcomp').find(".text-danger").text("");
            for (let e in errors.responseJSON["errors"]) {
                let campo = $('#agregarcomp').find("input[name=" + e + "]")
                campo.addClass("is-invalid")
                $('#' + e).text(errors.responseJSON['errors'][e])
            }


        }
    });
}



function registrarcp() {

    $.ajax({
        data: $("#agregarprov").serialize(),
        url: $("#agregarprov").attr('action'),
        type: $("#agregarprov").attr('method'),
        success: function(response) {
            location.reload();
        },
        error: function(errors) {
            $('#agregarprov').find(".text-danger").text("");
            for (let e in errors.responseJSON["errors"]) {
                let campo = $('#agregarprov').find("input[name=" + e + "]")
                campo.addClass("is-invalid")
                $('#' + e).text(errors.responseJSON['errors'][e])
            }


        }
    });
}

function registrarmp() {

    $.ajax({
        data: $("#editarprov").serialize(),
        url: $("#editarprov").attr('action'),
        type: $("#editarprov").attr('method'),
        success: function(response) {
            location.reload();
        },
        error: function(errors) {
            $('#editarprov').find(".text-danger").text("");
            for (let e in errors.responseJSON["errors"]) {
                let campo = $('#editarprov').find("input[name=" + e + "]")
                campo.addClass("is-invalid")
                $('#' + e).text(errors.responseJSON['errors'][e])
            }


        }
    });
}

function cambioestado(id) {
    let ids = id
    let token = $("#camestado").find('input[name=csrfmiddlewaretoken]').val()
    swal.fire({
        title: '¿Estás seguro de cambiar el estado de este proveedor?',
        text: "Al cambiar el estado no se podrá usar este proveedor mientras este inhabilitado",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Si, estoy seguro',
        cancelButtonText: 'No, cancelar!',
        reverseButtons: true
    }).then((willDelete) => {
        if (willDelete.isConfirmed) {
            $.ajax({
                data: { "csrfmiddlewaretoken": token, "estado": ids },
                url: $("#camestado").attr('action'),
                type: $("#camestado").attr('method'),
                success: function(data) {
                    swal.fire("Se ha modificado el proveedor", {
                        icon: 'success',
                    }).then(function() {
                        location.reload()
                    });
                },
                error: function(errors) {
                    alert("Error: kiwi perro " + errors.responseJSON)
                }
            });

        } else {
            location.reload()
        }
    });
}

function cambioestadoP(id) {
    let ids = id
    let token = $("#camestado").find('input[name=csrfmiddlewaretoken]').val()
    swal.fire({
        title: '¿Estás seguro de cambiar el estado de este producto?',
        text: "Al cambiar el estado no se podrá usar este producto mientras este inhabilitado",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Si, estoy seguro',
        cancelButtonText: 'No, cancelar!',
        reverseButtons: true
    }).then((willDelete) => {
        if (willDelete.isConfirmed) {
            $.ajax({
                data: { "csrfmiddlewaretoken": token, "estado": ids },
                url: $("#camestado").attr('action'),
                type: $("#camestado").attr('method'),
                success: function(data) {
                    swal.fire("Se ha modificado el producto", {
                        icon: 'success',
                    }).then(function() {
                        location.reload()
                    });
                },
                error: function(errors) {
                    Error = error['responseJSON']
                    Swal.fire({
                        icon: 'info',
                        title: 'Atención.',
                        text: Error['error'] + '.',
                    })
                }
            });

        } else {
            location.reload()
        }
    });
}


function cambioestadoTP(id) {
    let ids = id
    let token = $("#camestado").find('input[name=csrfmiddlewaretoken]').val()
    swal.fire({
        title: '¿Estás seguro de cambiar el estado de este tipo de producto?',
        text: "Al cambiar el estado no se podrá usar este tipo de producto mientras este inhabilitado",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Si, estoy seguro',
        cancelButtonText: 'No, cancelar!',
        reverseButtons: true
    }).then((willDelete) => {
        if (willDelete.isConfirmed) {
            $.ajax({
                data: { "csrfmiddlewaretoken": token, "estado": ids },
                url: $("#camestado").attr('action'),
                type: $("#camestado").attr('method'),
                success: function(data) {
                    swal.fire("Se ha modificado el tipo de producto", {
                        icon: 'success',
                    }).then(function() {
                        location.reload()
                    });
                },
                error: function(errors) {
                    alert("Error: kiwi perro " + errors.responseJSON)
                }
            });

        } else {
            location.reload()
        }
    });
}

// function sumartotal(){
//    cantidad = document.getElementById("cant").value
//    console.log(cantidad)
//    $.ajax({  
//      data: $(this).serialize(),
//     url: "..",
//     type: $(this).attr('method'),
//     success: function(response){
//       console.log("cambio")
//     },
//   });
//   n = document.getElementById("total");
//   n.value = parseInt("0"+this.value) + parseInt("0"+this.defaultValue);
//  this.defaultValue = this.value;
//   }