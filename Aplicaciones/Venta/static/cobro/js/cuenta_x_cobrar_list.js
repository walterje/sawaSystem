var tbCuenta;
$(function () {
    tbCuenta= $('#data').DataTable({
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
            {"data": "venta.cliente.cli"},
            {"data": "venta.fecha_venta"},
            {"data": "venta.tipo_venta"},
            {"data": "venta.fecha_plazo"},
            {"data": "monto_x_cobrar"},
            {"data": "saldo"},
            {"data": "estado"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-4,-3],
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
                    var  buttons = '<a rel="cob" class="btn btn-success btn-xs btn-flat"><i class="fas fa-search"></i></a> ';
                   
                    return buttons;
                }
                },
        ],
        
        initComplete: function (settings, json) {

        }
    });
    //list cobro
    $('#data tbody')
    .on('click', 'a[rel="cob"]',function(){
     var tr=tbCuenta.cell($(this).closest('td, li')).index();
     var data=tbCuenta.row(tr.row).data();
     console.log(data);
     $('#tblCob').DataTable({
         responsive: true,
         autoWidth: false,
         destroy: true,
         deferRender: true,
         ajax: {
             url: window.location.pathname,
             type: 'POST',
             data: {
                 'action': 'search_cob_ven',
                 'id': data.id
             },
             dataSrc: ""
         },
         columns: [
             {"data": "fecha_cobro"},
             {"data": "monto_cobrado"},
             {"data": "caja.nombre"},
             {"data": "user.nombre_usuario_completo"} ,
             {"data": "forma_cobro.descripcion"},
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
     $('#myModelCob').modal('show');
    });
   
});