function GuardarCita(){
    swal({
      title: "Estas seguro?",
      text: "Se modificaran los datos de la cita",
      icon: "warning",
      buttons: true,
      dangerMode: true,
    }).then((willDelete) => {
      if (willDelete) {
        swal("OK! Su cita ha sido modificada con exito", {
          icon: "success",
        }).then(function() {
        window.location.href = "/Ventas/Calendario/";
     });
      } else {
        swal("OK! Ningun dato de su cita se ha modificado");
      }
    });

        }

function CancelarCita(){
    swal({
        title: "Tenga cuidado!",
        text: "Esta opcion no se puede desaser!",
        icon: "warning",
        buttons: true,
      }).then((willDelete) => {
        if (willDelete) {
          swal("OK! Se ha cancelado su cita", {
            icon: "success",
          }).then(function() {
          window.location.href = "/Ventas/Calendario/";
       });
        } else {
          swal("OK! No se cancelo la cita ");
        }
      });
}

function ConfirmarNoGuardarCita(){
  swal({
    title: "Estas seguro?",
    text: "No se guardaran los cambios que haya hecho",
    icon: "warning",
    buttons: true,
    dangerMode: true,
  }).then((willDelete) => {
    if (willDelete) {
      swal("OK! Se redigira al listado de las citas", {
        icon: "error",
      }).then(function() {
      window.location.href = "/Ventas/ListadoCitas/";
   });
    } else {
      swal("OK! Puede seguir haciendo lo que estaba haciendo");
    }
  });
}

function GuardarCita(){
  swal({
    title: "Hecho",
    text: "Cita guardada",
    icon: "success",
  }).then(function() {
    window.location.href = "/Ventas/ListadoCitas/";
 });
}

function ConfirmarCita(id){
  let ids=id
  
    swal({
      title: "Estas seguro?",
      text: "Se modificara el estado de la cita",
      icon: "warning",
      buttons: true,
      dangerMode: true,
    }).then((changeStatus) => {
      if (changeStatus) {
        $(document).ready(function(){
        $.ajax({
          data: {"csrfmiddlewaretoken":csrftoken, "estado":ids},
          url: '/Ventas/CambiarEstadoCita/',
          type: 'POST',
          success: function(datas){
            swal("OK! Se ha confirmado la cita, en este momento se esta notificando al cliente", {
                icon: "success",
              }).then(function(){
                location.reload()
              });
          },
          error: function(error){
            swal("¡ERROR! ha ocurrido un error inesperado", {
              icon: "error",
            }).then(function(){
              location.reload()
            });
          }
        }); 
        })
      } else {
        swal("OK! no se han aplicado cambios").then(function(){
          location.reload()
        });
        
      }
    });
}
function CancelarCita3(id){
  let ids=id
  
    swal({
      title: "Estas seguro?",
      text: "Se cancelara la cita",
      icon: "warning",
      buttons: true,
      dangerMode: true,
    }).then((changeStatus) => {
      if (changeStatus) {
        $(document).ready(function(){
        $.ajax({
          data: {"csrfmiddlewaretoken":csrftoken, "estado":ids},
          url: '/Ventas/CambiarEstadoCita/',
          type: 'POST',
          success: function(datas){
            swal("OK! Se ha cancelado la cita, en este momento se esta notificando al cliente", {
                icon: "success",
              }).then(function(){
                location.reload()
              });
          },
          error: function(error){
            swal("¡ERROR! ha ocurrido un error inesperado", {
              icon: "error",
            }).then(function(){
              location.reload()
            });
          }
        }); 
        })
      } else {
        swal("OK! no se han aplicado cambios").then(function(){
          location.reload()
        });
        
      }
    });
}

function CancelarCita2(){
  swal({
      title: "Tenga cuidado!",
      text: "Esta opcion no se puede desaser!",
      icon: "warning",
      buttons: true,
    }).then((willDelete) => {
      if (willDelete) {
        swal("OK! Se ha cancelado su cita", {
          icon: "success",
        }).then(function() {
        window.location.href = "/Ventas/ListadoCitas/";
     });
      } else {
        swal("OK! No se cancelo la cita ");
      }
    });
}

// catalogo

function abrir_modal_detalleServicio(url){
  $("#VerMasServivios").load(url, function (){  
    $(this).appendTo("body").modal("show");
  });
}


