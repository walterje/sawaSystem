var tbCaja;
var tbAper;
var modal_title;

function getData() {
    tbCaja = $('#data').DataTable({
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
            {"data": "nombre"},
            {"data": "saldo_actual"},
            {"data": "estado"},
            {"data": "moneda.sigla"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return agregarSeparadorMiles(parseInt(data));
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                
                render: function (data, type, row) {
                
                    var buttons = '<a href="#" rel="edit" class="btn btn-warning btn-xs btn-flat btnEdit"><i class="fas fa-edit"></i></a> ';
                 
                    buttons += '<a href="#"  rel="delete" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    console.log(row);
                    if (row.estado=='Cerrado'){

                        buttons += '<a href="#" rel="aper" type="button" class="btn btn-blank btn-xs btn-plus"><i class="fas fa-key"></i></a>';
                    
                    }else{
                        buttons += '<a href="#" name="cerrar" rel="cierre" type="button" class="btn btn-blank"><i class="fas fa-lock"></i></i></i></a>';
                    
                    }
                    return buttons;                 
                    
                }
            },
        ],
        initComplete: function (settings, json) {

        }
        
    });
}

$(function () {

    modal_title = $('.modal-title');

    getData();
    //para crear la caja
    $('.btnAdd').on('click', function () {
        $('input[name="action"]').val('add');
        modal_title.find('span').html('Creación de una caja');
        console.log(modal_title.find('i'));
        modal_title.find('i').removeClass().addClass('fas fa-plus');
        $('form')[0].reset();
        $('#myModalCaja').modal('show');
    });
    //para editar la caja
    $('#data tbody')
    .on('click', 'a[rel="edit"]', function () {
        modal_title.find('span').html('Edición de caja');
        modal_title.find('i').removeClass().addClass('fas fa-edit');
        var tr = tbCaja.cell($(this).closest('td, li')).index();
        var data = tbCaja.row(tr.row).data();
        $('input[name="action"]').val('edit');
        $('input[name="id"]').val(data.id);
        $('input[name="nombre"]').val(data.nombre);
        $('#myModalCaja').modal('show');
    })
     //para aperturar la caja
    .on('click', 'a[rel="aper"]', function () {
        modal_title.find('span').html('Apertura de caja');
        modal_title.find('i').removeClass().addClass('fas fa-key');
        var tr = tbCaja.cell($(this).closest('td, li')).index();
        var data = tbCaja.row(tr.row).data();
       
        console.log($('input[name="action"]').val('aper'));
        $('input[name="id"]').val(data.id);
        $('input[name="nombre"]').val(data.nombre);
        $('input[name="monto_inicio"]').val(data.monto_inicio);
        $('#myModalAper').modal('show');
     })
     //para cerrar caja

    .on('click', 'a[rel="cierre"]', function () {
       
        modal_title.find('span').html('Cierre de caja');
        modal_title.find('i').removeClass().addClass('fas fa-lock');
        var tr = tbCaja.cell($(this).closest('td, li')).index();
        var data = tbCaja.row(tr.row).data();
        console.log(tr);
        console.log(data);
        console.log($('input[name="action"]').val('cierre'));
        $('input[name="id"]').val(data.id);
        $('input[name="nombre"]').val(data.nombre);
        $('input[name="saldo_actual"]').val(agregarSeparadorMiles(data.saldo_actual));
        $('input[name="monto_cierre"]').val(data.monto_cierre);
       
        $('#myModalCierre').modal('show');
     })
    //para eliminar
    .on('click', 'a[rel="delete"]', function () {
        var tr = tbCaja.cell($(this).closest('td, li')).index();
        var data = tbCaja.row(tr.row).data();
        var parameters = new FormData();
        parameters.append('action', 'delete');
        parameters.append('id', data.id);
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar eliminar el siguiente registro?', parameters, function () {
            tbCaja.ajax.reload();
        });
    });


    $('#myModalCaja').on('shown.bs.modal', function () {
       // $('form')[0].reset();
    });
   
    //$('#myModalCaja').modal('show');
    //
    $('form').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            $('#myModalCaja').modal('hide');
            $('#myModalAper').modal('hide');
            $('#myModalCierre').modal('hide');
            tbCaja.ajax.reload();
            Swal.fire({
                title: '',
                text: 'Se registro correctamente',
                icon: 'success',
                timer: 2000,
            }).then((result) => {

            });
        });
    });
});