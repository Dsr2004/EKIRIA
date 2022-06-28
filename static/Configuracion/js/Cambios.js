function ColorFondo1() {
    // const codigo = e.which || e.keyCode;
    // if (codigo === 13) {
    let ColorFondo = document.getElementById("ColorFondo").value;
    let body = document.getElementById("body-content-menu");
    body.style.backgroundColor = ColorFondo;
    // }

}

function CambioLetra1() {
    $(document).ready(function() {
        let TipoLetra = document.querySelector("#TipoLetra").value;
        let body = document.querySelectorAll(".tipo");
        body.forEach(texto => {
            if (texto.style.fontFamily = TipoLetra) {
                texto.style.fontFamily = TipoLetra
                texto = texto.style.fontFamily = TipoLetra;
                console.log(texto)
            }
        });
    })
}

function ColorLetra1() {
    // const codigo = event.which || event.keyCode;
    // if (codigo === 13) {
    $(document).ready(function() {
        let ColorLetra = document.querySelector("#ColorLetra").value;
        let texto = document.querySelectorAll(".content");
        texto.forEach(textos => {
            if (textos.style.color = ColorLetra) {
                textos.style.color = ColorLetra
                textos = textos.style.color = ColorLetra
            }
        });

    });
    // }
}


function CambiarTamano1(event) {
    const codigo = event.which || event.keyCode;
    if (codigo === 13) {
        $(document).ready(function() {
            let TamanoLetra = document.querySelector("#TamanoLetra").value;
            let tamano = document.querySelectorAll("#text");
            tamano.forEach(tamanos => {
                if (tamanos.style.fontSize = TamanoLetra) {
                    tamanos.style.fontSize = TamanoLetra + ("px")
                    tamanos = tamanos.style.fontSize = TamanoLetra + ("px")
                }
            });

        });
    }
}

function CambiarTamano2(event) {
    const codigo = event.which || event.keyCode;
    if (codigo === 13) {
        $(document).ready(function() {
            let TamanoLetra2 = document.querySelector("#TamanoLetra2").value;
            let tamano2 = document.querySelectorAll("#text2");
            tamano2.forEach(tamanos2 => {
                if (tamanos2.style.fontSize = TamanoLetra2) {
                    tamanos2.style.fontSize = TamanoLetra2 + ("px")
                    tamanos2 = tamanos2.style.fontSize = TamanoLetra2 + ("px")
                }
            });

        });
    }
}
// aqui esta el footer

function ColorFondoFooter2() {
    // const codigo = event.which || event.keyCode;
    // if (codigo === 13) {
    let ColorFondo2 = document.getElementById("ColorFondo2").value;
    let body2 = document.getElementById("texto2");
    body2.style.backgroundColor = ColorFondo2;
    // }

}

function ColorLetraFooter2() {
    // const codigo = event.which || event.keyCode;
    // if (codigo === 13) {
    $(document).ready(function() {
        let ColorLetra2 = document.querySelector("#ColorLetra2").value;
        let texto2 = document.querySelectorAll(".tipo2");
        texto2.forEach(textos2 => {
            if (textos2.style.color = ColorLetra2) {
                textos2.style.color = ColorLetra2
                textos2 = textos2.style.color = ColorLetra2;
            }
        });

    });
    // }
}

function CambiarTamanoFooter2(event) {
    const codigo = event.which || event.keyCode;
    if (codigo === 13) {
        $(document).ready(function() {
            let TamanoLetra3 = document.querySelector("#TamanoLetra3").value;
            let tamano3 = document.querySelectorAll("#text3");
            tamano3.forEach(tamanos3 => {
                if (tamanos3.style.fontSize = TamanoLetra3) {
                    tamanos3.style.fontSize = TamanoLetra3 + ("px")
                    tamanos3 = tamanos3.style.fontSize = TamanoLetra3 + ("px")
                }
            });

        });
    }
}

function CambiarTamano2Footer(event) {
    const codigo = event.which || event.keyCode;
    if (codigo === 13) {
        $(document).ready(function() {
            let TamanoLetra4 = document.querySelector("#TamanoLetra4").value;
            let tamano4 = document.querySelectorAll("#text4");
            tamano4.forEach(tamanos4 => {
                if (tamanos4.style.fontSize = TamanoLetra4) {
                    tamanos4.style.fontSize = TamanoLetra4 + ("px")
                    tamanos4 = tamanos4.style.fontSize = TamanoLetra4 + ("px")
                }
            });

        });
    }
}

function CambioLetraFooter2() {
    $(document).ready(function() {
        let TipoLetra = document.querySelector("#TipoLetra2").value;
        let body = document.querySelectorAll(".tipo2");
        body.forEach(texto => {
            if (texto.style.fontFamily = TipoLetra) {
                texto.style.fontFamily = TipoLetra
                texto = texto.style.fontFamily = TipoLetra
                console.log(texto)
            }
        });
    })
}

function ActualizarCambiosPagina() {
    const swalWithBootstrapButtons = Swal.mixin({
        customClass: {
            confirmButton: 'btn btn-success sweetAlertB',
            cancelButton: 'btn btn-danger sweetAlertB',
        },
        buttonsStyling: false
    })

    swalWithBootstrapButtons.fire({
        title: '¿Estas seguro?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Aceptar',
        cancelButtonText: 'Cancelar',
        reverseButtons: true
    }).then((result) => {
        if (result.isConfirmed) {
            $(document).ready(function() {
                $.ajax({
                    data: $("#cambiosPaginaForm").serialize(),
                    url: $("#cambiosPaginaForm").attr("action"),
                    type:$("#cambiosPaginaForm").attr("method"),
                    dataType: 'json',
                    success: function(response) {
                        swalWithBootstrapButtons.fire(
                            'Modificado Correctamente',
                            'Cambiaste el estado',
                            'success'
                        ).then(function() {
                            location.reload()
                        });
                    },
                    error: function(error){
                        $('#cambiosPaginaForm').find('.text-danger').text('')
                        $('#cambiosPaginaForm').removeClass('is-invalid')
                        for (let item in error.responseJSON["errores"]){
                            let input =$("#cambiosPaginaForm").find('input[name='+item+']')
                            input.addClass("is-invalid")
                            $('#'+item).text(error.responseJSON["errores"][item])
                            
                            // si imprime con esto  aun no veo el error
                            // aunque aun no dice que campo exactamente es el 
                            // error solo muestra dos errores si son dos campos
                            // alert(error.responseJSON["errores"][item])
                            
                    }
                    
                }
                });

            })

        } else if (
            /* Read more about handling dismissals below */
            result.dismiss === Swal.DismissReason.cancel
        ) {
            swalWithBootstrapButtons.fire(
                'Cancelado',
                'Ningun Cambio',
                'error'
            ).then(function() {
                location.reload()
            });
        }
    });

};

function ActualizarCambiosFooter() {
    const swalWithBootstrapButtons = Swal.mixin({
        customClass: {
            confirmButton: 'btn btn-success sweetAlertB',
            cancelButton: 'btn btn-danger sweetAlertB',
        },
        buttonsStyling: false
    })

    swalWithBootstrapButtons.fire({
        title: '¿Estas seguro?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Aceptar',
        cancelButtonText: 'Cancelar',
        reverseButtons: true
    }).then((result) => {
        if (result.isConfirmed) {
            $(document).ready(function() {
                $.ajax({
                    data: $("#CambiosFooterForm").serialize(),
                    url: $("#CambiosFooterForm").attr("action"),
                    type: $("#CambiosFooterForm").attr("method"),
                    dataType: 'json',
                    success: function(response) {
                        swalWithBootstrapButtons.fire(
                            'Modificado Correctamente',
                            'Cambiaste el estado',
                            'success'
                        ).then(function() {
                            location.reload()
                        });
                    },
                    error: function(error){
                        $("#CambiosFooterForm").find('.text-danger').text('')
                        $("#CambiosFooterForm").removeClass('is-invalid')
                        for (let item in error.responseJSON["errores"]){
                            let input =$("#CambiosFooterForm").find('input[name='+item+']')
                            input.addClass("is-invalid")
                            $('#'+item).text(error.responseJSON["errores"][item])
                            
                    }
                    
                }
                });

            })

        } else if (
            /* Read more about handling dismissals below */
            result.dismiss === Swal.DismissReason.cancel
        ) {
            swalWithBootstrapButtons.fire(
                'Cancelado',
                'Ningun Cambio',
                'error'
            ).then(function() {
                location.reload()
            });
        }
    });

};