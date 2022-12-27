var vent = {
    pr:{
        ordenV: [],

    },
    items: {
        ordenVenta : '',
        fecha_venta: '',
        tipo_venta: '',
        fecha_plazo: '',
        cliente: '',
        subtotal: 0,
        iva_0: 0,
        iva_5: 0,
        iva_10: 0,
        total: 0,
        productos: [],
    },
    add: function(item){
       this.items.productos.push(item);
       this.list() ;
    },
    list: function () {

        $('#tbProductos').DataTable({//para llamar al id=tbProductos
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.items.productos,
            columns: [
                {"data": "producto.nombre_producto"},
                {"data": "precio_venta"},
                {"data": "cantidad"},
                {"data": "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [-1,-3],
                        class: 'text-center',
                        orderable: false,
                        render: function (data, type, row) {
                            return '' +  agregarSeparadorMiles(parseInt(data));
                        }
                    
                },
            ],
            initComplete: function (settings, json) {

            }
        });
        
        $('#tbOrderV').DataTable({//para llamar al id=tbOrdenV
            responsive: true,
            autoWidth: false,
            destroy: true,
            order: false,
            paging: false,
            ordering: false,
            info: false,
            searching: false,
            dom: 'Bfrtip',
            data: this.pr.ordenV,//llama a mi diccionario orden
            columns: [
                {"data": "cliente.cli"},
                {"data": "iva_0"},
                {"data": "iva_5"},
                {"data": "iva_10"},
                {"data": "total"},
            ],
            columnDefs: [
                {
                    targets: [-1,-2,-3,-4],
                        class: 'text-center',
                        orderable: false,
                        render: function (data, type, row) {
                            return '' +  agregarSeparadorMiles(parseInt(data));
                        }
                    
                },
            ],
            initComplete: function (settings, json) {

            }
        });
        console.clear();
        console.log(this.items.productos);
        console.log('------');
        console.log(this.items);
    },
};
$(function () {
    //Select del tipo venta
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });
    //Fecha_venta
    $('#fecha_venta').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        //minDate: moment().format("YYYY-MM-DD")
    });
    //Fecha plazo
    $('#fecha_plazo').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
    });
    //para buscar orden venta
     $('input[name="search"]').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_orden_v',
                    'term': request.term
                },
                dataType: 'json',
            }).done(function (data) {
                response(data);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                //alert(textStatus + ': ' + errorThrown);
            }).always(function (data) {

            });
        },
        delay: 500,
        minLength: 1,
        select: function (event, ui) {
            event.preventDefault();
            console.clear();
            vent.pr.ordenV.length=0;
            vent.items.productos.length=0;
            //carga de vent
            vent.items.ordenVenta=(ui.item.id);
            vent.items.cliente=(ui.item.cliente.id);
            vent.items.subtotal=(ui.item.subtotal);
            vent.items.iva_0=(ui.item.iva_0);
            vent.items.iva_5=(ui.item.iva_5);
            vent.items.iva_10=(ui.item.iva_10);
            vent.items.total=(ui.item.total);
            vent.pr.ordenV.push(ui.item);
            for (i = 0; i < ui.item.det.length; i++) {
                vent.add(ui.item.det[i]);
            } 
            $(this).val('');
        }
    });
    //para limpiar el buscador
    $('.btnClearSearch').on('click', function () {
        $('input[name="search"]').val('').focus();
    });
    //para ocultar campo si es credito o debito
    var es_credito= $('select[name="tipo_venta"]');
    es_credito.on('change', function () {
        var container1 = $(this).parent().parent().find('input[name="fecha_plazo"]').parent();

        $(container1).hide();
        if (this.value=='1') {
            $(container1).show();
        }

    });
    //para agregar mi venta
    $('form').on('submit', function (e) {
        e.preventDefault();
        vent.items.fecha_venta = $('input[name="fecha_venta"]').val();
        vent.items.tipo_venta = $('select[name="tipo_venta"]').val();
        vent.items.fecha_plazo = $('input[name="fecha_plazo"]').val();
        if(vent.pr.ordenV.length === 0){
            Swal.fire('Debe cargar datos de la orden de venta ');
            return false;
        }
        if( vent.items.fecha_plazo < vent.items.fecha_venta){
            Swal.fire('La fecha plazo no puede ser menor que la fecha de venta');
            return false;
        }
       
        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        //console.log(parameters.append('action', $('input[name="action"]').val()));
        parameters.append('vent', JSON.stringify(vent.items));
      
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            //location.href = '/Venta/venta/list/';
            Swal.fire({
                title: '',
                text: 'Se registro correctamente',
                icon: 'success',
                timer: 2000,
                onClose: () => {
                    location.href = '/Venta/venta/list/';
                }
            }).then((result) => {

            });
        });
    });
    //venta.list();

});