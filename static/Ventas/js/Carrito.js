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
            title: "¿Estás seguro?",
            text: "Se borrara este servicio",
            icon: "warning",
            buttons: {
          confirm : {text:'Confirmar',className:'btn-success'},
          cancel : 'Cancelar'
      },
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
              swal("¡OK! No se borró el servicio que personalizo").then(function(){
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
  
  let cajaI = $("#containerInicio")
  let spinner = $("#spinnerLoad")
  let titulo = $("#titleSpinner")
  let form = $("#TerminarPedidoForm")

  cajaI.css("display", "none")
  spinner.removeClass("quitar")
  spinner.css("margin-top", "40vh")
  titulo.removeClass("quitar")
  titulo.css("margin-top", "15px")
  form.find('.text-danger').text('')
  form.find('.is-invalid').removeClass('is-invalid')


  $.ajax({
    data: form.serialize(),
    url: form.attr("action"),
    type: form.attr("method"),
    success: function(data){
      location.href="/Ventas/Calendario/"
    },
    error: function(error){
      $("#alertaError").removeClass("quitar")
      cajaI.css("display", "block")
      spinner.addClass("quitar")
      
      for (let i in error.responseJSON["errores"]){
        let x=form.find('input[name='+i+']')
        x.addClass("is-invalid")
        $("#"+i).text(error.responseJSON["errores"][i])
    }
    for (let i in error.responseJSON["errores"]){
      let x=form.find('select[name='+i+']')
      x.addClass("is-invalid")
      $("#"+i).text(error.responseJSON["errores"][i])
  }
      
    }
  });

}