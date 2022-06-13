 // Pone la tabla en español y responsive
 $(document).ready(function() {
     $('#Tabletipo_producto').DataTable({
         "language": {
             "url": "//cdn.datatables.net/plug-ins/1.10.16/i18n/Spanish.json"
         },
         responsive: true
     });
 });
 // Defino el elemento que estoy sosteniendo con el click y lo mando a la funcion Poner
 var id = 0
 const focus = document.querySelectorAll(".focus")
 focus.forEach(el => {
     el.addEventListener("mousedown", e => {
         let th = e.target
         let tr = th.parentNode
         let id = tr.getAttribute('id')
         var Tipo = document.getElementById(id);
         Poner(Tipo)
         Tipo = ""
     });
 });

 // defino cont como contador para inicializar la funcion Poner en 0 y así solo se ejecute una vez
 var cont = 0

 function Poner(Tipo) {
     const Cont = document.querySelector('#labelTp')
     const tbody = document.getElementById('tbody')
     var tipo_producto = document.getElementById('tipo_producto')
     Cont.addEventListener('dragover', e => {
         e.preventDefault();
     })
     var div = 0
     var tipo = ""
     var cont2 = 1
     if (cont == 0) {
         tipo = Tipo
     }
     cont = cont + 1
     Cont.addEventListener('drop', e => {
         if (cont2 == 1) {
             div = div + 1
             while (div == 1) {
                 // Obtengo el clon y el contenedor a almacenarlo
                 let DropCompra = document.getElementById('DropCompra')
                 var clon = tipo.cloneNode(true);
                 if (DropCompra.hasChildNodes()) {
                     var children = DropCompra.childNodes;
                     var boolean = []
                     children.forEach(child => {
                             if (child.innerHTML == clon.innerHTML) {
                                 boolean[0] = false
                             }
                         })
                         // Condiciono que solo se puede realizar el appendChild si no existe un bloque igual al que se intenta almacenar
                     if (boolean[0] != false) {
                         DropCompra.appendChild(clon);
                         let p = document.getElementById('pAlertContenedor')
                         p.style.display = "none"
                         let Alerta = document.getElementById('Alerta')
                         Alerta.style.display = "none"
                         DropCompra.style.display = "block"
                             // introduzco los demás input 
                         let cant = document.getElementById('cantidad' + id)
                         let inputcant = document.getElementById('inputcantidad' + id)
                         let cantclon = cant.cloneNode(true);
                         let precio = document.getElementById('precio' + id)
                         let inputprecio = document.getElementById('inputprecio' + id)
                         let precioclon = precio.cloneNode(true);
                         let close = document.getElementById('remove' + id)
                         let removeclon = close.cloneNode(true)
                         id = id + 1
                         cant.id = "cantidad" + id
                         precio.id = "precio" + id
                         close.id = 'remove' + id
                         let btn_close = close.lastChild
                         btn_close.lastChild.innerHTML = id
                         inputcant.id = "inputcantidad" + id
                         inputprecio.id = 'inputprecio' + id
                         DropCompra.lastChild.appendChild(cantclon)
                         DropCompra.lastChild.appendChild(precioclon)
                         DropCompra.lastChild.appendChild(removeclon)
                         keyPress(id - 1)
                     } else {
                         let p = document.getElementById('pAlertContenedor')
                         p.style.display = "block"
                     }
                 }
                 div = div + 1
                 cont2 = cont2 + 1
                 cont = 0
             }
         }
     })
 }

 function keyPress(id) {
     let precioInput = document.getElementById('inputprecio' + id)
     let cantInput = document.getElementById('inputcantidad' + id)
     precioInput.addEventListener('blur', e => {
         Valores()
     })
     cantInput.addEventListener('blur', e => {
         Valores()
     })
     try {
         const close = document.querySelectorAll(".closeButton")
         if (close) {
             close.forEach(btn => {
                 btn.parentNode.addEventListener('click', e => {
                     let i = e.target
                     let button = i.parentNode
                     if (button.classList[0] == 'btn') {
                         try {
                             let td = button.parentNode
                             let tr = td.parentNode
                             let tbody = tr.parentNode
                             let ids = tbody.getAttribute('id')
                             let secionC = document.getElementById(ids)
                             secionC.removeChild(tr)
                             let pk = document.getElementById(tr.id).id.substring(4)
                             let ClassCantidad = document.querySelectorAll('.cantidad')
                             cantidad = []
                             Precio = []
                             let DropCompra = document.getElementById('DropCompra')
                             var children = DropCompra.childNodes;
                             if (children[1] == undefined) {
                                 let Alerta = document.getElementById('Alerta')
                                 Alerta.style.display = "block"
                             }
                             for (let i = 0; i < ClassCantidad.length - 1; i++) {
                                 if (i != pk - 1) {
                                     identi = ClassCantidad[i].id.substring(13)
                                     let precioInput = document.getElementById('inputprecio' + identi).value
                                     let cantInput = document.getElementById('inputcantidad' + identi).value
                                     if (precioInput != "") {
                                         ValorNeto(i, cantInput, precioInput)
                                     }
                                 }
                             }
                             Calcular()
                         } catch (error) {}
                     }
                 })
             })
         }
     } catch (ex) {}
 }

 cantidad = []
 Precio = []
 PrecioNeto = []
 CantidadNeta = []
 ValorTotal = []
 ValorTotal[0] = 0

 function Valores() {
     let ClassCantidad = document.querySelectorAll('.cantidad')
     for (let i = 0; i < ClassCantidad.length - 1; i++) {
         identi = ClassCantidad[i].id.substring(13)
         let precioInput = document.getElementById('inputprecio' + identi).value
         let cantInput = document.getElementById('inputcantidad' + identi).value
         if (precioInput != "" && cantInput != "") {
             ValorNeto(i, cantInput, precioInput)
         }
     }
     Calcular()
 }

 function ValorNeto(id, cant, precio) {
     cantidad[id] = cant
     Precio[id] = precio
 }

 function Calcular() {
     ValorTotal[0] = 0
     PrecioNeto = []
     CantidadNeta = []
     for (let i = 0; i < Precio.length; i++) {
         PrecioNeto[i] = Number(Precio[i])
         CantidadNeta[i] = Number(cantidad[i])
     }
     for (let i = 0; i < PrecioNeto.length; i++) {
         valorNp = Number(PrecioNeto[i]) * Number(CantidadNeta[i])
         ValorTotal[0] = Number(ValorTotal[0]) + valorNp
     }
     // Definir contenedor de almacenaje Total
     let contdivTotal = document.getElementById('contenTotal')
     let contenedorTotal = document.getElementById('TotalNeto')
     if (isNaN(ValorTotal[0])) {
         contenedorTotal.innerHTML = "Calculando..."
     } else {
         contenedorTotal.innerHTML = "$" + ValorTotal[0]
     }
     if (ValorTotal[0] != 0) {
         contdivTotal.style.display = "block"

     } else {
         contdivTotal.style.display = "none"
     }
     PrecioNeto = []
     CantidadNeta = []
     cantidad = []
     Precio = []

 }