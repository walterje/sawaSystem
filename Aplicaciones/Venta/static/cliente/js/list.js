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
            },
            dataSrc: "",
            headers: {
                'X-CSRFToken': csrftoken
            }
        },
        columns: [
            {"data": "posicion"},
            {"data": "nombre"},
            {"data": "apellido"},
            {"data": "ci"},
            {"data": "telefono"},
            {"data": "direccion"},
            {"data": "sexo"},
            {"data": "posicion"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/Venta/cliente/edit/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/Venta/cliente/delete/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
            {
                targets: [-5],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                //return parseFloat(data).toFixed(0) + ' Gs.' ;
                     return agregarSeparadorMiles(data);
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
});