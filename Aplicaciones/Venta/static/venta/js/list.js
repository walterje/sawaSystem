var tbVenta;
$(function () {
    tbVenta = $('#data').DataTable({
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
            {"data": "fecha_venta"},
            {"data": "tipo_venta"},
            {"data": "fecha_plazo"},
            {"data": "cliente.cli"},
            //{"data": "subtotal"},
            {"data": "total"},
            {"data": "posicion"},
        ],
        columnDefs: [
            {
                
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '' +  agregarSeparadorMiles(parseInt(data));
                },
            },
            {  
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a rel="details" class="btn btn-secondary btn-xs btn-flat">Det</a>';
                    buttons += '<a href="/Venta/venta/pdf/'+row.id+'/" target="_blank" class="btn btn-info btn-xs btn-flat"><i class="fas fa-file-pdf"></i></a> ';
                    
                    //buttons += '<a href="#" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
            
        ],
        initComplete: function (settings, json) {

        }
    });
    //list detalle 
    $('#data tbody')
        .on('click', 'a[rel="details"]',function(){
        var tr=tbVenta.cell($(this).closest('td, li')).index();
        var data=tbVenta.row(tr.row).data();
        console.log(data);
 
        $('#tblDet').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_details_prod',
                    'id': data.id
                },
                dataSrc: ""
            },
            columns: [
                {"data": "producto.nombre_producto"},
                {"data": "precio_venta"},
                {"data": "cantidad"},
                {"data": "subtotal"},
                ],
                columnDefs: [
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return data;
                    }
                },
                {
                    targets: [-3,-1],
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
        $('#myModelDet').modal('show');//para llamarle al modal de mi detalle
    });    

});