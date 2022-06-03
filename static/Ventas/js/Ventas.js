 //ELIMINAR TIPO DE SERVICIO 
 function abrir_modal_calendario(url){ 
  $("#ModalCitaCalendario").load(url, function (){ 
    $(this).appendTo("body").modal('show');
  });
}

function GuardarCita(){
    swal({
      title: "¿Estás seguro?",
      text: "Se modificaran los datos de la cita",
      icon: "warning",
      buttons: {
          confirm : {text:'Confirmar',className:'btn-success'},
          cancel : 'Cancelar'
      },
      dangerMode: true,
    }).then((willDelete) => {
      if (willDelete) {
        swal("¡OK! Su cita ha sido modificada con exito", {
          icon: "success",
        }).then(function() {
        window.location.href = "/Ventas/Calendario/";
     });
      } else {
        swal("¡OK! Ningún dato de su cita se ha modificado");
      }
    });

        }

function CancelarCita(){
    swal({
        title: "Tenga cuidado!",
        text: "¡Esta opcion no se puede desaser!",
        icon: "warning",
        buttons: {
          confirm : {text:'Confirmar',className:'btn-success'},
          cancel : 'Cancelar'
      },
      }).then((willDelete) => {
        if (willDelete) {
          swal("¡OK! Se ha cancelado su cita", {
            icon: "success",
          }).then(function() {
          window.location.href = "/Ventas/Calendario/";
       });
        } else {
          swal("¡OK! No se cancelo la cita ");
        }
      });
}l

function ConfirmarNoGuardarCita(){
  swal({
    title: "¿Estás seguro?",
    text: "No se guardaran los cambios que haya hecho",
    icon: "warning",
    buttons: {
          confirm : {text:'Confirmar',className:'btn-success'},
          cancel : 'Cancelar'
      },
    dangerMode: true,
  }).then((willDelete) => {
    if (willDelete) {
      swal("¡OK! Se redigira al listado de las citas", {
        icon: "error",
      }).then(function() {
      window.location.href = "/Ventas/ListadoCitas/";
   });
    } else {
      swal("¡OK! Puede seguir haciendo lo que estaba haciendo");
    }
  });
}

function IraModificarCita(url){
  swal({
    title: "¡Cuidado!",
    text: "Está a punto de modificar datos sensibles.",
    icon: "info",
    buttons: {
          confirm : {text:'Confirmar',className:'btn-success'},
          cancel : 'Cancelar'
      },
    dangerMode: true,
  }).then((done) =>{
    if (done){
      location.href = url
     }
     else{
       swal.close()
     }
  })
}

function ConfirmarCita(id){
  let ids=id
  
    swal({
      title: "¿Estás seguro?",
      text: "Se modificara el estado de la cita",
      icon: "warning",
      buttons: {
          confirm : {text:'Confirmar',className:'btn-success'},
          cancel : 'Cancelar'
      },
      dangerMode: true,
    }).then((changeStatus) => {
      if (changeStatus) { 
        $(document).ready(function(){
          let cajaI = $("#containerInicio")
          let spinner = $("#spinnerLoad")
          let titulo = $("#titleSpinner") 
          cajaI.css("display", "none")
          spinner.removeClass("quitar")
          spinner.css("margin-top", "40vh")
          titulo.removeClass("quitar")
          titulo.css("margin-top", "15px")

        $.ajax({
          data: {"csrfmiddlewaretoken":csrftoken, "estado":ids},
          url: '/Ventas/CambiarEstadoCita/',
          type: 'POST',
          success: function(datas){
            cajaI.css("display", "block")
            spinner.addClass("quitar")
            spinner.css("margin-top", "0vh")
            titulo.addClass("quitar")
            titulo.css("margin-top", "0px")

            swal("¡OK! Se ha confirmado la cita, en este momento se está notificando al cliente", {
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
        swal("¡OK! no se han aplicado cambios").then(function(){
          location.reload()
        });
        
      }
    });
}

function ActualizarCita(id){
  let ids=id
  
    swal({
      title: "¿Estás seguro?",
      text: "Se modificara  la cita",
      icon: "warning",
      buttons: {
          confirm : {text:'Confirmar',className:'btn-success'},
          cancel : 'Cancelar'
      },
      dangerMode: true,
    }).then((changeStatus) => {
      if (changeStatus) {
        $(document).ready(function(){
          form = $("#EditarCitaForm")
        $.ajax({
          data: form.serialize(),
          url: form.attr("action"),
          type: 'POST',
          success: function(datas){
            swal({
              title: "¡Está hecho!",
              text: "Se modifico  la cita",
              icon: "success",
            }).then((update)=>{
              location.href = "/Ventas/Calendario/"
            })
          },
          error: function(error){
            if (error.responseJSON["errores"]["empleado_id"]){
              $("#DiaCitaBox").css("display", "none")
              $("#horaInicioBox").css("display", "none")
            }
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
        })
      } else {
        swal("¡OK! no se han aplicado cambios").then(function(){
          location.reload()
        });
        
      }
    });
}

function ActualizarCita2(id){
  let ids=id
  
    swal({
      title: "¿Estás seguro?",
      text: "Se modificara  la cita",
      icon: "warning",
      buttons: {
          confirm : {text:'Confirmar',className:'btn-success'},
          cancel : 'Cancelar'
      },
      dangerMode: true,
    }).then((changeStatus) => {
      if (changeStatus) {
        $(document).ready(function(){
          ruta = '/Ventas/EditarCita/'+ids
          form = $("#EditarCitaForm")
        $.ajax({
          data: form.serialize(),
          url: form.attr("action"),
          type: 'POST',
          success: function(datas){
            swal({
              title: "¡Está hecho!",
              text: "Se modifico  la cita",
              icon: "success",
            }).then((update)=>{
              location.href = "/Ventas/ListadoCitas/"
            })
          },
          error: function(error){
            wal({
              title: "¡HO NO!",
              text: "Ha ocurrido un error",
              icon: "error",
            }).then((update)=>{
              location.href = "/Ventas/Calendario/"
            })
          }
        }); 
        })
      } else {
        swal("¡OK! no se han aplicado cambios").then(function(){
          location.reload()
        });
        
      }
    });
}

function CancelarCita3(id){
  swal({
      title: "Tenga cuidado!",
      text: "¡Está opcion no se puede desaser!",
      icon: "warning",
      buttons: {
          confirm : {text:'Confirmar',className:'btn-success'},
          cancel : 'Cancelar'
      },
    }).then((willDelete) => {
      if (willDelete) {
        let cajaI = $("#containerInicio")
        let spinner = $("#spinnerLoad")
        let titulo = $("#titleSpinner")
      
        cajaI.css("display", "none")
        spinner.removeClass("quitar")
        spinner.css("margin-top", "40vh")
        titulo.removeClass("quitar")
        titulo.css("margin-top", "15px")
         
        $.ajax({
          data: {"csrfmiddlewaretoken":csrftoken, "cita":id},
          url: '/Ventas/CancelarCita/',
          type: 'POST',
          success: function(data){
            cajaI.css("display", "block")
            spinner.addClass("quitar")
            spinner.css("margin-top", "0vh")
            titulo.addClass("quitar")
            titulo.css("margin-top", "0px")
            swal("¡OK! Se ha cancelado su cita", {
              icon: "success",
            }).then(function() {
            window.location.href = "/Ventas/Calendario/";
         });
          },
          error: function(error){
            swal("ha habido un error", {
              icon: "error",
            }).then(function() {
            window.location.href = "/Ventas/Calendario/";
         });
          }
        })
       
      } else {
        swal("¡OK! No se cancelo la cita ");
      }
    });
}

function CancelarCita2(id){
  swal({
      title: "Tenga cuidado!",
      text: "¡Está opcion no se puede desaser!",
      icon: "warning",
      buttons: {
          confirm : {text:'Confirmar',className:'btn-success'},
          cancel : 'Cancelar'
      },
    }).then((willDelete) => {
      if (willDelete) {
        let cajaI = $("#containerInicio")
        let spinner = $("#spinnerLoad")
        let titulo = $("#titleSpinner")
      
        cajaI.css("display", "none")
        spinner.removeClass("quitar")
        spinner.css("margin-top", "40vh")
        titulo.removeClass("quitar")
        titulo.css("margin-top", "15px")
         
        $.ajax({
          data: {"csrfmiddlewaretoken":csrftoken, "cita":id},
          url: '/Ventas/CancelarCita/',
          type: 'POST',
          success: function(data){
            cajaI.css("display", "block")
            spinner.addClass("quitar")
            spinner.css("margin-top", "0vh")
            titulo.addClass("quitar")
            titulo.css("margin-top", "0px")
            swal("¡OK! Se ha cancelado la cita del cliente", {
              icon: "success",
            }).then(function() {
            window.location.href = "/Ventas/ListadoCitas/";
         });
          },
          error: function(error){
            swal("ha habido un error", {
              icon: "error",
            }).then(function() {
            window.location.href = "/Ventas/ListadoCitas/";
         });
          }
        })
       
      } else {
        swal("¡OK! No se cancelo la cita ");
      }
    });
}

// catalogo

function abrir_modal_detalleServicio(url){
  $("#VerMasServivios").load(url, function (){  
    $(this).appendTo("body").modal("show");
  });
}

function abrir_modal_img_servicioPer(modalAabrir){
  $("#"+modalAabrir).appendTo("body").modal("show");
}

