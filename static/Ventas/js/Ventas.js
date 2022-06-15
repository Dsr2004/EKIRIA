
$(function(){
  $("input[name='RangoFecha']").daterangepicker({
    locale:{
      applyLabel:"<i class='fa-solid fa-chart-pie'></i> Generar Reporte",
      cancelLabel:"<i class='fa-solid fa-xmark'></i> Cancelar"

    },
    applyButtonClasses: "btn-success",
    cancelButtonClasses: "btn-danger",
  });

  $("input[name='RangoFecha']").on('apply.daterangepicker', function(ev, picker) {
    let datos = {"csrfmiddlewaretoken":csrftoken, "fechaInicio":picker.startDate.format('YYYY-MM-DD'), "fechaFin":picker.endDate.format('YYYY-MM-DD'), "accion":"GenerarReporte"}
    $.ajax({
      data: datos,
      url: "/Ventas/Reportes/CitasPDF/",
      type: "POST",
      success: function(datas){
        window.open(datas);
      },
      error: function(error){
        swal("¡Error!","No se pudo generar el reporte","error")
      }
    }); 
});
});

 
 //ELIMINAR TIPO DE SERVICIO 
 function abrir_modal_calendario(url){ 
  $("#ModalCitaCalendario").load(url, function (){ 
    $(this).appendTo("body").modal('show');
  });
}

function PersonalizarServAgendarCitaModal(){
  $("#ServicioPersonalizadoCita").appendTo("body").modal('show');
}

function abrir_modal_reporte_empleado(){
  $("#ModalReporteEmpleado").appendTo("body").modal("show");
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
}

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
              location.href = "/Ventas/DetalleEditarCita/"+ids
            })
          },
          error: function(error){
            wal({
              title: "¡HO NO!",
              text: "Ha ocurrido un error",
              icon: "error",
            }).then((update)=>{
              location.href = "/Ventas/DetalleEditarCita/"+ids
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
// Agendar citas por parte del admin
function BuscarUsuarioParaCita(){
  let form = $("#BuscarUsuarioForm")
  let busqueda = $("#busqueda").val()
  $.ajax({
    data: {"csrfmiddlewaretoken":csrftoken, "busqueda":busqueda, "accion":"BuscarUsuario"},
    url: form.attr("action"),
    type: form.attr("method"),
    dataType: 'json',
    success: function(data){
     for(i in data){
       usuario = data[i]
     }
    },
    error: function(error){
      console.log(error)
    }
  })
}

// AGENDAR CITA POR PARTE DEL ADMIN

 var ServiciosCitaTable = $('#ServiciosTable').DataTable()
 $('#ServiciosPersonalizadosTable').DataTable()

$("#AgregarServicioPerForm").on("submit", function(e){
  e.preventDefault()
  let form = $(this)
  let tipo_servicio =form.find("#id_tipo_servicio_id").val()
  let img = form.find("#id_img_servicio").prop("files")[0]
  let urlImg = form.find("#id_img_servicio").val()
  let descripcion = form.find("#id_descripcion").val()
  var validImageTypes = ["image/jfif", "image/jpeg", "image/png"];

  if (tipo_servicio == "") {
    swal("¡Error!", "Debe seleccionar un tipo de servicio", "error")
  }else if (img == undefined) {
    swal("¡Error!", "Debe seleccionar una imagen", "error")
  }else if ($.inArray(img["type"], validImageTypes) < 0) {
    swal("¡Error!", "Debe seleccionar una imagen valida", "error")
}else if(isNaN(tipo_servicio)){
  swal("¡Error!", "Debe seleccionar un tipo de servicio valido", "error")
}else if(tipo_servicio != "1" && tipo_servicio != "2"){
    swal("¡Error!", "Debe seleccionar un tipo de servicio dentro del rango", "error")
}else{
  try{
    tipo_servicio = parseInt(tipo_servicio)
  }catch(error){
    swal("¡Error!", "Debe seleccionar un tipo de servicio valido", "error")
  }

  if (tipo_servicio == 1) {
    var nombreTipo ="Manicure"
  }else if (tipo_servicio == 2) {
    var nombreTipo ="Pedicure"
  }
  let formDataPer = {
      "tipo_servicio_id":tipo_servicio,
      "tipo_servicio_nombre":nombreTipo,
      "img_servicio":img,
      "descripcion": descripcion,
      "urlImg": urlImg
    }

  citaObject.addPersonalizado(formDataPer)
  $("#AgregarServicioPerForm").trigger("reset")
  $("#ServicioPersonalizadoCita").modal("hide")
}
})

var citaObject = {
  items:{
    cliente: '',
    empleado:'',
    dia:'',
    hora:'',
    descricpion:'',
    total:0,
    items:'',
    servicios:[],
    serviciosPersonalizados:[],
    id:[],
    objServiciosPersonalizados:[],

  },
  add : function(item){
    id = item["id_servicio"]
    if (this.items.id.length == 0) {
      this.items.id.push(id)
      this.items.servicios.push(item)
      this.items.total += parseInt(item["precio"])
      $("#TotalPedido").html("$"+this.items.total)
    }else{
      if (!this.items.id.includes(id)) {
        this.items.servicios.push(item)
        this.items.id.push(id)
        this.items.total += parseInt(item["precio"])
        $("#TotalPedido").html("$"+this.items.total)
      }else{
        console.log("ya esta")
      }
    }
    this.items.items= this.items.servicios.length+this.items.serviciosPersonalizados.length
    this.list()
  },
  list: function(){
    $("#ItemsPedido").html(this.items.items)
    tblServices =  $('#ServiciosTable').DataTable({
      "language": {
        "url": "//cdn.datatables.net/plug-ins/1.10.16/i18n/Spanish.json"
    },
      responsive: true,
      autoWidth: false,
      destroy: true,
      data: this.items.servicios,
      columns: [
          {"data": "img_servicio"},
          {"data": "nombre"},
          {"data": "tipo_servicio_id"},
          {"data": "precio"},
          {"data": "id_servicio"},
      ],
      columnDefs: [
          {
              targets: [-1],
              class: 'text-center',
              orderable: false,
              render: function (data, type, row) {
                  return '<a rel="quitar" class="btn btn-danger btn-xs btn-flat" style="color: white;"><i class="fas fa-trash-alt"></i></a>';
              }
          },
          {
            targets: [0],
            class: 'text-center',
            orderable: false,
            render: function (data, type, row) {
                return '<img src="'+row.img_servicio+'" style="border-radius: 15px;" width="80" height="50">'
            }
        },
          
      ],
      initComplete: function (settings, json) {

      }
  });
  },
  addPersonalizado : function(item){
    let id = {"id":this.items.serviciosPersonalizados.length}
    let personalizado = item
    $.extend(personalizado, id)
    this.items.serviciosPersonalizados.push(personalizado)
    this.items.items= this.items.servicios.length+this.items.serviciosPersonalizados.length
    this.listPersonalizado()
  },
  listPersonalizado: function(){
    $("#ItemsPedido").html(this.items.items)
    tblServices =  $('#ServiciosPersonalizadosTable').DataTable({
      "language": {
        "url": "//cdn.datatables.net/plug-ins/1.10.16/i18n/Spanish.json"
    },
      responsive: true,
      autoWidth: false,
      destroy: true,
      data: this.items.serviciosPersonalizados,
      columns: [
          {"data": "tipo_servicio_nombre"},
          {"data": "descripcion"},
          {"data": "id"},
      ],
      columnDefs: [
          {
              targets: [-1],
              class: 'text-center',
              orderable: false,
              render: function (data, type, row) {
                  return '<a rel="quitar" class="btn btn-danger btn-xs btn-flat" style="color: white;"><i class="fas fa-trash-alt"></i></a>';
              }
          },
         
          
      ],
      initComplete: function (settings, json) {

      }
  });
  },
  calcularTotal: function(){
    $("#TotalPedido").html("$"+citaObject.items.total)
  }
}

function formatRepo (repo) {
  if (repo.loading) {
    return repo.text;
  }

  var $container = $(
    '<div class="row select2-result-repository clearfix">'+
    '<div class="col-md-2"><img src="'+repo.imagen+'" alt="" width="100" style="border-radius: 30px;"></div>'+
    '<div class="col-md-2"></div>'+
    '<div class="col-md-8">'+
        '<div class="row" style="margin-top:10px;" >'+
            '<h6><strong>Nombre: </strong> '+ repo.text+' </h6>'+
            '<h6><strong>Nombre de Usuario:  </strong>'+repo.nombreUser+'</h6>'+
            '<h6 style="color:red;"><strong style="color:black; ">Rol:  </strong>'+repo.rol+'</h6>'+
        '</div>'+
    '</div>'+
'</div>'

  );

  return $container;
}

function formatRepoAfterSelection (repo) {
  if (repo.loading) {
    return repo.text;
  }

  var $container = $(
    '<div class="row select2-result-repository clearfix" style="max-height:200px; overflow-y:auto"; overflow-x:none>'+
    '<div class="col-2"><img src="'+repo.imagen+'" alt="" width="100" style="border-radius: 30px; text-align: center;"></div>'+
    '<div class="col-2"></div>'+
    '<div class="col-8">'+
        '<div class="row" style="margin-top:10px;" >'+
            '<h6 style="word-break: break-all;"><strong>Nombre: </strong> '+ repo.text+' </h6>'+
            '<h6 style="word-break: break-all;"><strong>Nombre de Usuario:  </strong>'+repo.nombreUser+'</h6>'+
            '<h6 style="word-break: break-all;"><strong>Correo: </strong> '+ repo.email+' </h6>'+
            '<h6 style="word-break: break-all;"><strong>Telefono:  </strong>'+repo.celular+'</h6>'+
        '</div>'+
    '</div>'+
'</div>'

  );

  return $container;
}
function repetirUsuarioFuncion(){
  $("#EsconderDespuesSelectUser").css("display", "block");
  $("#MostarDespuesSelectUser").html("");
  $("#RepetirUsuarioBoton").css("display", "none");
  $('select[name="cliente_id"]').val(null).trigger('change');
 
}
$(document).ready(function() {
  // buscar usuario 
  $('select[name="cliente_id"]').select2({
    theme: 'bootstrap4',
    language: "es",
    ajax: {
      delay:250,
      type:'POST',
      url: window.location.pathname,
      data: function(params){
        return {"csrfmiddlewaretoken":csrftoken, "busqueda":params.term, "accion":"BuscarUsuario"}
      },
      processResults: function(data){
        return {results: data}
      },
    },
    placeholder: 'Busque por nombre de usuario o correo',
    minimumInputLength: 1,
    templateResult: formatRepo,
  }).on("select2:select", function(e){
    $("#EsconderDespuesSelectUser").css("display", "none");
    $("#MostarDespuesSelectUser").html(formatRepoAfterSelection(e.params.data));
    $("#RepetirUsuarioBoton").css("display", "block");
  })

  // buscar servicios 

  $('input[name="buscarServicio"]').autocomplete({
    source: function(request, response) {
      $.ajax({
        url: window.location.pathname,
        type: "POST",
        data: {"csrfmiddlewaretoken":csrftoken, "busqueda":request.term, "accion":"BuscarServicio"},
        dataType: "json",
      }).done(function(data){
        response(data);
      }).fail(function(jqXHR, textStatus, errorThrown){

      });
    },
    minLength: 1,
    delay: 250,
    select: function(event, ui) {
      event.preventDefault();
      citaObject.add(ui.item)
      $(this).val("")
    }
  });
  $("#ServiciosTable tbody").on("click","a[rel=quitar]", function(){
    console.log(citaObject.items.servicios)
    var precio = $(this).closest("tr").find("td:eq(3)").text();
    precio = parseInt(precio)
    var tr = $(this).closest("td, li").index();
    citaObject.items.servicios.splice(tr.row, 1);
    citaObject.items.total = citaObject.items.total - precio;
    console.log(citaObject.items.total)
    $("#TotalPedido").html("$"+citaObject.items.total)
    citaObject.list()
   
  })
});

$("#agregarCitaForm").on("submit", function(e){
  e.preventDefault();
  // asignacion de datos faltantes
  citaObject.items.cliente = $(this).find("select[name='cliente_id']").val();
  citaObject.items.empleado = $(this).find("select[name='empleado_id']").val();
  citaObject.items.dia = $(this).find("input[name='diaCita']").val();
  citaObject.items.hora = $(this).find("input[name='horaInicioCita']").val();
  citaObject.items.descricpion  = $(this).find("textarea[name='descripcion']").val();

  // defninicion de variables para el envio de datos
  let datos = JSON.stringify(citaObject.items);
  let personalizados = citaObject.items.serviciosPersonalizados
  var form = new FormData();
  form.append("csrfmiddlewaretoken", csrftoken);
  form.append("accion", "AgregarCita");
  form.append("cita", datos);
  if (personalizados.length > 0) {
    $(personalizados).each(function(index, value){
      form.append("serviciosPersonalizados["+index+"]", value);
      form.append("imgServiciosPersonalizados["+index+"]", citaObject.items.serviciosPersonalizados[index].img_servicio);
    })
  }
  form.append("serviciosPersonalizados", citaObject.items.serviciosPersonalizados)

  // enviando los datos a la vista 
  $.ajax({
    url: window.location.pathname,
    type: "POST",
    data: form,
    contentType: false,
    processData: false,
    success: function(data){
      if(data.status == "ok"){
        alert("Cita agregada correctamente");
        
      }
    },error: function(jqXHR, textStatus, errorThrown){
      alert("Error al agregar la cita");
    }
  });
})