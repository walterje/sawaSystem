var tbProductos;
var orden_v={
    items:{//un diccionario con todos los componente de mi cabezera y mi detalle de orden venta
        fecha_orden_v:'',
        cliente:'',
        estado:'',
        subtotal:0,
        subtotal_iva_0:0,
        subtotal_iva_5:0,
        subtotal_iva_10:0,
        iva_0:0,
        iva_5:0,
        iva_10:0,
        total: 0,
        productos: []//array para  guardar los detalles de mi orden     
    },
    calculate_orden_venta: function () {
        var subtotal=0;
        var subtotal_0=0;
        var subtotal_5=0;
        var subtotal_10=0;
        var iva_0=0;
        var iva_5=0;
        var iva_10=0;
     
        $.each(this.items.productos,function(pos,dict)
        {   
            console.log(pos);
            dict.pos=pos;
            console.log(dict);
            console.log(dict.precio_venta);
            console.log(dict.iva);
           
            dict.subtotal = dict.cantidad * parseInt(dict.precio_venta);//subtotal de mi orden
            subtotal += dict.subtotal;
           
            if(dict.iva=='0'){
                dict.subtotal_0= dict.cantidad * parseInt(dict.precio_venta);//subtotal de mi orden
                subtotal_0 += dict.subtotal_0;
                iva_0=subtotal_0*0;
                
            }else if(dict.iva=='1'){
                dict.subtotal_5= dict.cantidad * parseInt(dict.precio_venta);//subtotal de mi orden
                subtotal_5 += dict.subtotal_5;
                iva_5=parseInt(subtotal_5*0.047619);
                
            }else if(dict.iva=='2'){
                dict.subtotal_10= dict.cantidad * parseInt(dict.precio_venta);//subtotal de mi orden
                subtotal_10 += dict.subtotal_10;
                iva_10=parseInt(subtotal_10*0.090909);

                
            }

            console.log(subtotal);
            console.log(subtotal_0);
            console.log(subtotal_5);
            console.log(subtotal_10);

        });
        this.items.subtotal = parseInt(subtotal);
        this.items._iva_0 = iva_0;
        this.items.iva_5= iva_5;
        this.items.iva_10 = iva_10;
        this.items.total = parseInt(this.items.subtotal);
        console.log(this.items.subtotal);
        console.log(this.items.iva_0);
        console.log(this.items.iva_5);
        console.log(this.items.iva_10);
        

        $('input[name="subtotal"]').val(agregarSeparadorMiles(this.items.subtotal));//para agregar al subtotal de mi detalle
        $('input[name="iva_0"]').val(agregarSeparadorMiles(this.items.iva_0));
        $('input[name="iva_5"]').val(agregarSeparadorMiles(this.items.iva_5));
        $('input[name="iva_10"]').val(agregarSeparadorMiles(this.items.iva_10));
        $('input[name="total"]').val(agregarSeparadorMiles(this.items.total));
    
    },
    add: function(item){
        console.log(item.tipo_producto.id === 1 && item.cant_stock === 0);
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
               
				Swal.fire('Este producto ya agregaste');
			}else{
				// Si no existe lo agregamos
				this.items.productos.push(item);
			}
            
            
		};
		this.list();
    },
    list: function () {
        this.calculate_orden_venta();
        tbProductos=$('#tbProductos').DataTable({//para llamar al id=tbProductos
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.items.productos,//lama a mi diccionario producto
            columns: [
                {"data": "id"},
                {"data": "nombre_producto"},
                {"data": "tipo_producto.nombre"},
                {"data": "precio_venta"},
                {"data": "cantidad"},
                {"data": "subtotal"},
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
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '' + agregarSeparadorMiles(parseInt(data));
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cantidad" class="form-control form-control-sm" autocomplete="off" value="'+row.cantidad+'">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '' + agregarSeparadorMiles(parseInt(data));
                    }
                },
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {
            if(data.tipo_producto.id === 1){
                $(row).find('input[name="cantidad"]').TouchSpin({
                    min: 1,
                    max: data.cant_stock,
                    step: 1
                });
            }else{
                $(row).find('input[name="cantidad"]').TouchSpin({
                    min: 1,
                    max: 50,
                    step: 1
                });
            }

            },
            initComplete: function (settings, json) {

            }
        });
       // console.clear();
        console.log(this.items);
        //console.log(this.get_ids());
    },
};


$(function () {
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });
    //fecha orden venta
    var fecha_orden_v = $('input[name="fecha_orden_v"]');
    fecha_orden_v.datetimepicker({
        useCurrent: false,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
    });
    fecha_orden_v.datetimepicker('date', fecha_orden_v.val());


    // search clients

    $('select[name="cliente"]').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: window.location.pathname,
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: 'search_clientes'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese el nombre o ci del cliente',
        minimumInputLength: 1,
    });
    $('.btnAddCliente').on('click', function () {
        $('#myModalCliente').modal('show');
    });

    $('#myModalCliente').on('hidden.bs.modal', function (e) {
        $('#formCliente').trigger('reset');
    })

    $('#formCliente').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', 'create_cliente');
        submit_with_ajax(window.location.pathname, 'Notificación',
            '¿Estas seguro de crear al siguiente cliente?', parameters, function (response) {
                console.log(response);
                var newOption = new Option(response.nombre_completo, response.id, false, true);
                $('select[name="cliente"]').append(newOption).trigger('change');
                $('#myModalCliente').modal('hide');
            });
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
                    //'ids': JSON.stringify(orden_v.get_ids()),
                    
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
            event.preventDefault();//para detener el evento y continuar con los demas items sino no me permitiria
            console.clear();//a medida que se crea para que se limpie la consola
            ui.item.cantidad = 1;//o podriamos poner directo en la vista
            ui.item.subtotal = 0;
            console.log('-----');
            console.log(ui.item.tipo_producto.id===1);
            console.log(ui.item.cant_stock===0);
            if(ui.item.tipo_producto.id===1 && ui.item.cant_stock===0){
                Swal.fire('Producto Sin Stock');
            }else{
                console.log(orden_v.items);
                orden_v.add(ui.item);//se va agregar el producto y se va alistar automaticamente a travez de la funcion add
                $(this).val('');

            }
           
        }
    });
    //eliminar los productos de mi listado
    $('#tbProductos tbody')
        .on('click','a[rel="remove"]',function () {
            var tr =tbProductos.cell($(this).closest('td, li')).index();
            alert_action('Notificación', '¿Estas seguro de eliminar?',
                function () {
                    orden_v.items.productos.splice(tr.row,1);
                    orden_v.list();
                });
        }) 
        //cantidad
        .on('change', 'input[name="cantidad"]', function () {
        console.clear();
        var cantidad = parseInt($(this).val());
        var tr = tbProductos.cell($(this).closest('td, li')).index();
        orden_v.items.productos[tr.row].cantidad = cantidad;
        console.log(cantidad);
        console.log((cantidad > orden_v.items.productos[tr.row].cant_stock) && (orden_v.items.productos[tr.row].tipo_producto.id === 1));
       if((orden_v.items.productos[tr.row].tipo_producto.id === 1)){
        if((cantidad > orden_v.items.productos[tr.row].cant_stock) ){
            Swal.fire('Cantidad disponible solo ' + ' '+ orden_v.items.productos[tr.row].cant_stock);
        }
    }
        console.log(orden_v.items.productos[tr.row].cant_stock);
        orden_v.calculate_orden_venta();
        $('td:eq(5)', tbProductos.row(tr.row).node()).html('' + agregarSeparadorMiles(orden_v.items.productos[tr.row].subtotal));
        });
        //para limpiar el buscador
    $('.btnClearSearch').on('click', function () {
        $('input[name="search"]').val('').focus();
    }); 
    // event submit
    $('#formOrdenV').on('submit', function (e) {
        e.preventDefault();

        if(orden_v.items.productos.length === 0){
            Swal.fire('Debe cargar al menos un producto ');
            return false;
        }
        orden_v.items.fecha_orden_v = $('input[name="fecha_orden_v"]').val();
        orden_v.items.cliente = $('select[name="cliente"]').val();
        orden_v.items.estado = $('select[name="estado"]').val();
        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('orden_v', JSON.stringify(orden_v.items));
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            //location.href = '/Venta/ordenVenta/list/';
            Swal.fire({
                title: '',
                text: 'Se registro correctamente',
                icon: 'success',
                timer: 2000,
                onClose: () => {
                    location.href = '/Venta/ordenVenta/list/';
                }
            }).then((result) => {

            });
        });
    });


    orden_v.list();
    
});