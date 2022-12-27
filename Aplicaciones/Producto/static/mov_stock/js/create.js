var tbProductos;
var mov_stock={
    items:{//un diccionario con todos los componente de mi cabezera y mi detalle de orden compra
        fecha_mov:'',
        descripcion:'',
        productos: []//array para  guardar los detalles de mi orden     
    },
    add: function(item){
        //Validamos que sea el primer item en el listado
        if (this.items.productos.length == 0){
			this.items.productos.push(item);
		}else{
			// creamos un listado con los id de los items
			listado = [];
			$.each(this.items.productos, function (index, value){
				// Recorremos y guardamos en la lista temporal
				listado.push(value.id);
			});
			// Preguntamos si existe el id en la lista temporal
			if (listado.includes(item.id)){
				//alertMsg('El producto ya existe');
			}else{
				// Si no existe lo agregamos
				this.items.productos.push(item);
			}
		};
		this.list();
        
    },
    list: function () {
        tbProductos=$('#tbProductos').DataTable({//para llamar al id=tbProductos
            responsive: true,
            autoWidth: false,
            destroy: true,
            order: false,
            paging: false,
            ordering: false,
            info: false,
            searching: false,
            dom: 'Bfrtip',
            data: this.items.productos,//lama a mi diccionario producto
            columns: [
                {"data": "id"},
                {"data": "nombre_producto"},
                {"data": "cant_stock"},
                {"data": "cantidad"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat" style="color:white ;"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cantidad" class="form-control form-control-sm" autocomplete="off" value="'+row.cantidad+'">';
                    }
                },
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {

                $(row).find('input[name="cantidad"]').TouchSpin({
                    min: 1,
                    max: data.cant_stock,
                    step: 1
                });

            },
            initComplete: function (settings, json) {

            }
        });
    },
};


$(function () {
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });
    //fecha mov_stock
    $('#fecha_mov').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        //minDate: moment().format("YYYY-MM-DD")
    });
    //busqueda de producto
    $('input[name="search"]').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_products',
                    'term': request.term
                    //'ids': JSON.stringify(orden_c.get_ids()),
                    
                },
                dataType: 'json',
            }).done(function (data) {
                response(data);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                
            }).always(function (data) {

            });
        },
        delay: 500,
        minLength: 1,
        select: function (event, ui) {
            console.log(ui.item)
            event.preventDefault();//para detener el evento y continuar con los demas items sino no me permitiria
            console.clear();//a medida que se crea para que se limpie la consola
            mov_stock.items.productos.length=0;
            ui.item.cantidad = 1;//o podriamos poner directo en la vista
            console.log(mov_stock.items);
            mov_stock.add(ui.item);//se va agregar el producto y se va alistar automaticamente a travez de la funcion add
            $(this).val('');
        }
    });
    //eliminar los productos de mi listado
    $('#tbProductos tbody')
        .on('click','a[rel="remove"]',function () {
            var tr =tbProductos.cell($(this).closest('td, li')).index();
            alert_action('Notificación', '¿Estas seguro de eliminar?',
                function () {
                    mov_stock.items.productos.splice(tr.row,1);
                    mov_stock.list();
                });
        }) 
        //cantidad
        .on('change', 'input[name="cantidad"]', function () {
        console.clear();
        var cantidad = parseInt($(this).val());
        var tr = tbProductos.cell($(this).closest('td, li')).index();
        mov_stock.items.productos[tr.row].cantidad = cantidad;
      });
        //para limpiar el buscador
    $('.btnClearSearch').on('click', function () {
        $('input[name="search"]').val('').focus();
    }); 
    // event submit
    $('form').on('submit', function (e) {
        e.preventDefault();

        if(mov_stock.items.productos.length === 0){
            message_error('Debe cargar al menos un producto ');
            return false;
        }

        mov_stock.items.fecha_mov = $('input[name="fecha_mov"]').val();
        mov_stock.items.descripcion= $('input[name="descripcion"]').val();
        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('mov_stock', JSON.stringify(mov_stock.items));
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            //location.href = '/Compra/ordenCompra/list/';
            Swal.fire({
                title: '',
                text: 'Se registro correctamente',
                icon: 'success',
                timer: 2000,
                onClose: () => {
                    location.href = '/Producto/producto/list/';
                }
            }).then((result) => {

            });
        });
    });

mov_stock.list();
});