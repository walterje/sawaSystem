$(function () {
    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            }, // parametros
            dataSrc: ""
        },
        columns: [
            { "data": "posicion"},
            { "data": "caja.nombre"},
            { "data": "fecha_movimiento"},
            { "data": "descripcion"},
            { "data": "tipo_movimiento"},
            { "data": "monto_inicio"},
            { "data": "monto_ingreso"},
            { "data": "monto_egreso"},
            { "data": "monto_cierre"},
            //{ "data": "id"},//para los botones
        ],
        columnDefs: [
            {
                targets: [-2,-1,-3,-4],
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

});