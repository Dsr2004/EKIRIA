function BorrarNotificacion(url){
    swal({
        title: "¿Estás seguro?",
        text: "Se borrará la notificación, esta acción no se puede deshacer.",
        icon: "warning",
        buttons: {
          confirm : {text:'Confirmar',className:'btn-success'},
          cancel : 'Cancelar'
      },
        dangerMode: true,
    }).then((willDelete) => {
        if (willDelete) {
        window.location.href = url;
        } else {
        swal("¡OK! No se ha eliminado la notificación");
        }
    });
}

function filtrarNotificacion(tipo){
    if(tipo == "leido"){
        $("input[name=tipo]").val("leido")
    }else if(tipo == "Noleido"){
        $("input[name=tipo]").val("Noleido")
    }
   $("#FormFilter").submit()
}