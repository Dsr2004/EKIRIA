function abrir_modal_editar(url){
    $("#EditarRol").load(url, function(){
        $(this).appendTo("body").modal('show');
    });
}
function EditarRol(){
    $.ajax({
        data:$('#EditarRoles').serialize(),
        url:$('#EditarRoles').attr('action'),
        type:$('#EditarRoles').attr('method'),
        dataType: 'json',
        success: function (response) {
            location.reload()
        },
        error: function(error){
            $('#EditarRoles').find('.text-danger').text('')
            $('#EditarRoles').removeClass('is-invalid')
            for (let item in error.responseJSON["errores"]){
                let input =$("#EditarRoles").find('input[name='+item+']')
                alert('error')
                input.addClass("is-invalid")
                $('#'+item).text(error.responseJSON["errores"][item])
                
        }
        
    }
    });
}
