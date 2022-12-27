var tbCaja;
var mov_caja={
    items:{
        fecha_movimiento:'',
        descripcion:'',
        monto: '',
        caja: []  
    },
    add: function(item){
        //Validamos que sea el primer item en el listado
        if (this.items.caja.length == 0){
			this.items.caja.push(item);
		}else{
			// creamos un listado con los id de los items
			listado = [];
			$.each(this.items.caja, function (index, value){
				// Recorremos y guardamos en la lista temporal
				listado.push(value.id);
			});
			// Preguntamos si existe el id en la lista temporal
			if (listado.includes(item.id)){
				//alertMsg('El producto ya existe');
			}else{
				// Si no existe lo agregamos
				this.items.caja.push(item);
			}
		};
		this.list();
        
    },
    list: function () {
        tbCaja=$('#tbCaja').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            order: false,
            paging: false,
            ordering: false,
            info: false,
            searching: false,
            dom: 'Bfrtip',
            data: this.items.caja,//lama a mi diccionario producto
            columns: [
                {"data": "nombre"},
                {"data": "saldo_actual"},
                {"data": "monto"},
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="monto" class="form-control form-control-sm" autocomplete="off" value="'+row.monto+'">';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '' +  agregarSeparadorMiles(parseInt(data));
                    }
                },
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {
                $(row).find('input[name="monto"]').TouchSpin({
                    min: 0,
                    max: data.saldo_actual,
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
    //fecha mov_egreso_egreso
    $('#fecha_movimiento').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        //minDate: moment().format("YYYY-MM-DD")
    });
    //busqueda de caja abierta
    $('input[name="search"]').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_caja',
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
            mov_caja.items.caja.length=0;
            ui.item.monto = 0;//o podriamos poner directo en la vista
            console.log(mov_caja.items);
            mov_caja.add(ui.item);//se va agregar el producto y se va alistar automaticamente a travez de la funcion add
            $(this).val('');
        }
    });
  
    $('#tbCaja tbody')
        //monto
        .on('change', 'input[name="monto"]', function () {
            console.clear();
            var monto = parseInt($(this).val());
            var tr = tbCaja.cell($(this).closest('td, li')).index();
            mov_caja.items.caja[tr.row].monto = monto;
        });
        //para limpiar el buscador
         $('.btnClearSearch').on('click', function () {
            $('input[name="search"]').val('').focus();
        }); 
        // event submit
        $('form').on('submit', function (e) {
            e.preventDefault();

            if(mov_caja.items.caja.length === 0){
                message_error('Debe cargar al menos un item ');
                return false;
            }
            mov_caja.items.fecha_movimiento = $('input[name="fecha_movimiento"]').val();
            mov_caja.items.descripcion= $('input[name="descripcion"]').val();
            var parameters = new FormData();
            parameters.append('action', $('input[name="action"]').val());
            parameters.append('mov_caja', JSON.stringify(mov_caja.items));
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            //location.href = '/Compra/ordenCompra/list/';
            Swal.fire({
                title: '',
                text: 'Se registro correctamente',
                icon: 'success',
                timer: 2000,
                onClose: () => {
                    location.href = '/Caja/movimientoCaja/list/';
                }
            }).then((result) => {

            });
            });
        });

    mov_caja.list();
});