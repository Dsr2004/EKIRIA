function abrir_modal_crear(url){
    $("#CreateRol").load(url, function(){
        $(this).appendTo("body").modal('show');
    });
}
function CrearRol(){
    let name = document.getElementById('id_name').value
    let tipo = document.getElementById('tipo').value
    $.ajax({
        data:{"csrfmiddlewaretoken":csrftoken, "name":name, "tipo":tipo},
        url:$('#CrearRoles').attr('action'),
        type:$('#CrearRoles').attr('method'),
        dataType: 'json',
        success: function (response) {
            Swal.fire({
                position: 'top-end',
                icon: 'success',
                title: 'Creado Correctamente',
                showConfirmButton: false,
                timer: 1500
              })
              window.setTimeout(function(){ 
                location.reload();
            } ,1000);
        },
        error: function(error){
            $('#CrearRoles').find('.text-danger').text('')
            $('#CrearRoles').removeClass('is-invalid')
            for (let item in error.responseJSON["errores"]){
                let input =$("#CrearRoles").find('input[name='+item+']')
                input.addClass("is-invalid")
                $('#'+item).text(error.responseJSON["errores"][item])
                
        }
        
    }
    });
}

