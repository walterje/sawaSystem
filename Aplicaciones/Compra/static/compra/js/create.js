var comp = {
    
    pr:{
        ordenC: [],

    },
    items: {
        ordenCompra : '',
        fecha_compra: '',
        tipo_compra: '',
        fecha_plazo: '',
        nro_factura:'',
        proveedor: '',
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
                {"data": "precio"},
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
        
        $('#tbOrderC').DataTable({//para llamar al id=tbOrdenC
            responsive: true,
            autoWidth: false,
            destroy: true,
            order: false,
            paging: false,
            ordering: false,
            info: false,
            searching: false,
            dom: 'Bfrtip',
            data: this.pr.ordenC,//llama a mi diccionario orden
            columns: [
                {"data": "proveedor.nombre"},
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
    //Select del tipo compra
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });
    //Fecha_compra
    $('#fecha_compra').datetimepicker({
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
    //para buscar orden compra
     $('input[name="search"]').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_orden_c',
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
            comp.pr.ordenC.length=0;
            comp.items.productos.length=0;
            //carga de comp
            comp.items.ordenCompra=(ui.item.id);
            comp.items.proveedor=(ui.item.proveedor.id);
            comp.items.subtotal=(ui.item.subtotal);
            comp.items.iva_0=(ui.item.iva_0);
            comp.items.iva_5=(ui.item.iva_5);
            comp.items.iva_10=(ui.item.iva_10);
            comp.items.total=(ui.item.total);
            comp.pr.ordenC.push(ui.item);
            console.log(comp.pr.ordenC);
            for (i = 0; i < ui.item.det.length; i++) {
                comp.add(ui.item.det[i]);
            } 
            $(this).val('');
        }
    });
    //para limpiar el buscador
    $('.btnClearSearch').on('click', function () {
        $('input[name="search"]').val('').focus();
    });
    //para ocultar campo si es credito o debito
    var es_credito= $('select[name="tipo_compra"]');
    es_credito.on('change', function () {
        var container1 = $(this).parent().parent().find('input[name="fecha_plazo"]').parent();

        $(container1).hide();
        if (this.value=='1') {
            $(container1).show();
        }

    });
    //para agregar mi compra
    $('form').on('submit', function (e) {
        e.preventDefault();
        comp.items.fecha_compra = $('input[name="fecha_compra"]').val();
        comp.items.tipo_compra = $('select[name="tipo_compra"]').val();
        comp.items.fecha_plazo = $('input[name="fecha_plazo"]').val();
        comp.items.nro_factura = $('input[name="nro_factura"]').val();
      
        if(comp.pr.ordenC.length === 0){
            message_error('Debe cargar el nro de la orden ');
            return false;
        }
        if( comp.items.fecha_plazo < comp.items.fecha_compra){
            Swal.fire('La fecha plazo no puede ser menor que la fecha de compra');
            return false;
        }
        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        //console.log(parameters.append('action', $('input[name="action"]').val()));
        parameters.append('comp', JSON.stringify(comp.items));
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            //location.href = '/Compra/list/';
            Swal.fire({
                title: '',
                text: 'Se registro correctamente',
                icon: 'success',
                timer: 2000,
                onClose: () => {
                    location.href = '/Compra/list/';
                }
            }).then((result) => {

            });
        });
    });
    //compra.list();

});