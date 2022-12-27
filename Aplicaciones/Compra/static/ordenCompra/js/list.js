var tbOrden;
$(function () {
    tbOrden = $('#data').DataTable({
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
            {"data": "fecha_orden"},
            {"data": "proveedor.nombre"},
            {"data": "estado"},
            {"data": "iva_0"},
            {"data": "iva_5"},
            {"data": "iva_10"},
            {"data": "total"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-2, -3, -4,-5],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '' + agregarSeparadorMiles(parseInt(data));
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var  buttons = '<a rel="details" class="btn btn-secondary btn-xs btn-flat">Det</a> ';
                    buttons += '<a href="/Compra/ordenCompra/pdf/'+row.id+'/" target="_blank" class="btn btn-info btn-xs btn-flat"><i class="fas fa-file-pdf"></i></a> ';
                   
                    ///buttons += '<a href="/Compra/ordenCompra/' + row.id  + '/" class="btn btn-secondary btn-xs btn-flat">OC</a> ';          
                    
                    //buttons += '<a href="/Compra/ordenCompra/edit/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    //buttons += '<a href="/Compra/ordenCompra/delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a> ';
                   //buttons += '<a href="/Compra/ordenCompra/pdf/'+row.id+'/" target="_blank" class="btn btn-info btn-xs btn-flat"><i class="fas fa-file-pdf"></i></a> ';
                   //if (row.estado!='Cerrado'){ 
                       // buttons += '<a href="#" rel="confir" type="button" class="btn btn-blank btn-xs btn-plus"><i class="fas fa-edit"></i></a>';
                   //}
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
        var tr=tbOrden.cell($(this).closest('td, li')).index();
        var data=tbOrden.row(tr.row).data();
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
                {"data": "precio"},
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
        $('#myModelDet').modal('show');
     })  
        //para confirmar la anulacion
        .on('click', 'a[rel="confir"]', function () {
            //modal_title.find('span').html('Apertura de caja');
            //modal_title.find('i').removeClass().addClass('fas fa-key');
            var tr = tbOrden.cell($(this).closest('td, li')).index();
            var data = tbOrden.row(tr.row).data();
            console.log(tr);
            console.log(data);
            //Swal.fire('Estas seguro de anular')
            console.log($('input[name="action"]').val('confir'));
            $('input[name="id"]').val(data.id);
            $('input[name="proveedor"]').val(data.proveedor.nombre);
            $('select[name="estado"]').val(data.estado);
            $('#myModalConfir').modal('show');
           
        })
        $('form').on('submit', function (e) {
            e.preventDefault();
            var parameters = new FormData(this);
            submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de cambiar estado', parameters, function () {
                $('#myModalConfir').modal('hide');
                Swal.fire({
                    title: '',
                    text: 'Se ha modificado correctamente',
                    icon: 'success',
                    timer: 2000,
                }).then((result) => {
                    location.href = '/Compra/ordenCompra/list/';
                });
            });
        });

});

    