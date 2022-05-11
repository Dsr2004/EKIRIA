var UpdateBoton = document.getElementsByClassName('addToCar')

for(var i=0 ; i<UpdateBoton.length; i++){
    UpdateBoton[i].addEventListener('click', function(){
        var servicioID = this.dataset.servicio
        var accion = this.dataset.action
        console.log('servicioID ',servicioID, 'accion ',accion)

        if(user === "AnonymousUser"){
            console.log("User is not logged in")
        }else{
            ActualizarPedidoDeUsuario(servicioID,accion)
            console.log("Usuario logueado, enviando datos")
        }
    })
}

function ActualizarPedidoDeUsuario(servicioId, accion){ 
    var url = "/Ventas/AddtoCarrito/"
    if (accion == "removePer"){
        swal({
            title: "Estas seguro?",
            text: "Se borrara este servicio",
            icon: "warning",
            buttons: true,
            dangerMode: true,
          }).then((changeStatus) => {
            if (changeStatus) {
              $(document).ready(function(){
                $.ajax({
                    data: {"csrfmiddlewaretoken":csrftoken, "servicioId":servicioId, "accion":accion},
                    url: url,
                    type: "POST",
                    success: function(datas){
                        location.href="/Ventas/Carrito/"
                    },
                    error: function(error){
                     alert("ocurrio un error inseperado")
                    }
                  });
                 
              })
            } else {
              swal("OK! No se borró el servicio que personalizo").then(function(){
                location.reload()
              });
              
            }
          });
    }else if(accion == "updatePer"){
        
    }
    else{
        $.ajax({
            data: {"csrfmiddlewaretoken":csrftoken, "servicioId":servicioId, "accion":accion},
            url: url,
            type: "POST",
            success: function(datas){
                location.href="/Ventas/Carrito/"
            },
            error: function(error){
              return error.json()
            }
          });
    }
    
    
 }

 function abrir_modal_serviciosPersonalizados(url){
    $("#ActualizarServicioPer").load(url, function (){ 
       $(this).appendTo("body").modal('show');
     });
 }


function EnviarTerminarPedido(){
  let caja = $("#conteinerFinal")
  caja.addClass("cajadeCarga")
}