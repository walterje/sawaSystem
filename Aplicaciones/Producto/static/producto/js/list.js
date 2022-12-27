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
            { "data": "posicion"},//id
            { "data": "tipo_producto.nombre"},
            { "data": "nombre_producto"},
            { "data": "cant_stock"},
            { "data": "stock_minimo"},
            { "data": "precio_compra"},
            { "data": "precio_venta"},
            //{ "data": "iva"},
            { "data": "iva"},//para los botones
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/Producto/producto/edit/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/Producto/producto/delete/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return agregarSeparadorMiles(parseInt(data)) ;
                }
            },
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return agregarSeparadorMiles(parseInt(data));
                }
            },
            {
                targets: [-5],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    if (row.tipo_producto.nombre ==='Servicios') {
                        return '<span class="badge badge-secondary"> </span>';
                    }
                    if(row.cant_stock <= row.stock_minimo){  

                        return '<span class="badge badge-danger">'+data+'</span>'

                    }
                    return agregarSeparadorMiles(parseInt(data));
                }
            },
        ],
        initComplete: function (settings, json) {
          

        }
        
    });
   

});