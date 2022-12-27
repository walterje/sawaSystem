var tbCta;
$(function () {
    tbCta = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "posicion"},
            {"data": "id"},
            {"data": "compra.proveedor.nombre"},
            {"data": "compra.fecha_compra"},
            {"data": "compra.tipo_compra"},
            {"data": "compra.fecha_plazo"},
            {"data": "monto_x_pagar"},
            {"data": "saldo"},
            {"data": "estado"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-3,-4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '' +  agregarSeparadorMiles(parseInt(data));
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var  buttons = '<a rel="pag" class="btn btn-success btn-xs btn-flat"><i class="fas fa-search"></i></a> ';
                   
                    return buttons;
                }
                },
        ],
        
        initComplete: function (settings, json) {

        }
    });
    //list pago
       $('#data tbody')
       .on('click', 'a[rel="pag"]',function(){
        var tr=tbCta.cell($(this).closest('td, li')).index();
        var data=tbCta.row(tr.row).data();
        console.log(data);
        $('#tblPag').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_pag_comp',
                    'id': data.id
                },
                dataSrc: ""
            },
            columns: [
                {"data": "fecha_pago"},
                {"data": "monto_pagado"},
                {"data": "caja.nombre"},
                {"data": "user.nombre_usuario_completo"} ,
                {"data": "forma_pago.descripcion"},
                {"data": "efectivo"},
                {"data": "vuelto"},
                ],
                columnDefs: [
              
                {
                    targets: [-1,-2,-6],
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
        $('#myModelPag').modal('show');
       });
      
});