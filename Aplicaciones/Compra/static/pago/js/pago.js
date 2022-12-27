var tbCtaXPg;
var pag_cta = {
    items: {
        cta_x_pagar: '',
        fecha_pago: '',
        montopag:0,
        caja:'',
        forma_pago:'',
        saldo_actual: 0,
        vuelto: 0,
        efectivo:0,
        cta:[],
    },
    
    calculate_monto_pag: function () {
        var saldo_actual = 0;
        var vuelto = 0;
        $.each(this.items.cta, function (pos, dict) {
            dict.pos = pos;
            dict.saldo_actual = dict.saldo - parseInt(dict.montopag);
            saldo_actual += dict.saldo_actual;
           
            dict.vuelto = dict.efectivo - parseInt(dict.montopag);
            console.log(dict.vuelto);
            vuelto +=  dict.vuelto;
        });
        this.items.saldo_actual = saldo_actual;
        $('input[name="saldo_actual"]').val(agregarSeparadorMiles(this.items.saldo_actual));
        this.items.vuelto= vuelto;
        $('input[name="vuelto"]').val(agregarSeparadorMiles(this.items.vuelto));  
    },
    add: function(item){
        this.items.cta.push(item);
        console.log(this.items);
        this.list();
    },
    list: function () {
        this.calculate_monto_pag();
        tbCtaXPg=$('#tbCtaXPg').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            order: false,
            paging: false,
            ordering: false,
            info: false,
            searching: false,
            dom: 'Bfrtip',
            data: this.items.cta,
            columns: [
                {"data": "compra.proveedor.nombre"},
                {"data": "compra.fecha_compra"},
                {"data": "saldo"},
                {"data": "montopag"},
                {"data": "saldo_actual"},
                {"data": "efectivo"},
                {"data": "vuelto"},
                
            ],
            columnDefs: [
            
                {
                    targets: [-1,-3,-5],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '' +  agregarSeparadorMiles(parseInt(data));
                    }
                },
                {
                    targets: [-4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="montopag" class="form-control form-control-sm" autocomplete="off" value="'+row.montopag+'">';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="efectivo" class="form-control form-control-sm" autocomplete="off" value="'+row.efectivo+'">';
                    }
                },
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {

                $(row).find('input[name="montopag"]').TouchSpin({
                    min: 0,
                    max: data.saldo,
                    step: 1
               });
    
                $(row).find('input[name="efectivo"]').TouchSpin({
                    min: 0,
                    max: 10000000000,
                    step: 1
                });
            },
            initComplete: function (settings, json) {

            }
        });
    },
};

$(function () {
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });

    $('#fecha_pago').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
     
    });
   
    
    // search cta_x_pagar

    $('input[name="search"]').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_cta_x_pagar',
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
            pag_cta.items.cta.length=0;
            ui.item.montopag = 0;
            ui.item.efectivo = 0;
            ui.item.vuelto = 0;
            pag_cta.items.cta_x_pagar=(ui.item.id);
            ui.item.saldo_actual= ui.item.saldo;
            console.log(ui.item);
            pag_cta.add(ui.item);
            console.log(pag_cta.items);
            $(this).val('');
        }
    });
   
         //para limpiar el buscador
    $('.btnClearSearch').on('click', function () {
        $('input[name="search"]').val('').focus();
    }); 
     // event montopag

    $('#tbCtaXPg').on('change', 'input[name="montopag"]', function () {
        console.clear();
        var montopag = parseInt($(this).val());
        var tr = tbCtaXPg.cell($(this).closest('td, li')).index();
        if((pag_cta.items.cta[tr.row].compra.tipo_compra==0) && (montopag != pag_cta.items.cta[tr.row].monto_x_pagar)){
            Swal.fire('Verifique el monto su compra es contado ')
        }
        pag_cta.items.cta[tr.row].montopag = montopag;
        pag_cta.calculate_monto_pag();
        $('td:eq(4)', tbCtaXPg.row(tr.row).node()).html( agregarSeparadorMiles(pag_cta.items.cta[tr.row].saldo_actual.toFixed(0)));

    });
    //efectivo
 
    $('#tbCtaXPg').on('change', 'input[name="efectivo"]', function () {
        console.clear();
        var efectivo = parseInt($(this).val());
        var tr = tbCtaXPg.cell($(this).closest('td, li')).index();
        if( (pag_cta.items.cta[tr.row].montopag > efectivo)){
            Swal.fire('Verifique el monto del Efectivo');
            return false;
        }
        pag_cta.items.cta[tr.row].efectivo = efectivo;
        pag_cta.calculate_monto_pag();
       $('td:eq(6)', tbCtaXPg.row(tr.row).node()).html( agregarSeparadorMiles(pag_cta.items.cta[tr.row].vuelto.toFixed(0)));
     
   
    });

    // para guardar mi orden  pago
    $('form').on('submit', function (e) {
        e.preventDefault();
    
        if(pag_cta.items.cta.length === 0){
            message_error('Debe cargar un numero de cuenta');
            return false;
        }
        if(pag_cta.items.cta[0].montopag === 0){
    
            Swal.fire('<p>Debe ingresar el monto a pagar</p>');
            return false;
        }
       console.log(pag_cta.items.cta[0].compra.tipo_compra === '0');
        
        
        pag_cta.items.fecha_pago = $('input[name="fecha_pago"]').val();
        pag_cta.items.caja= $('select[name="caja"]').val();
        pag_cta.items.forma_pago= $('select[name="forma_pago"]').val();
        pag_cta.items.montopag=(pag_cta.items.cta[0].montopag);
        pag_cta.items.efectivo=(pag_cta.items.cta[0].efectivo);
        if((pag_cta.items.montopag != pag_cta.items.cta[0].saldo) && (pag_cta.items.fecha_pago == pag_cta.items.cta[0].compra.fecha_plazo)){
            if(pag_cta.items.cta[0].compra.tipo_compra==1){
            Swal.fire('Su plazo vence hoy')
            return false;
            }
    
        }
        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('pag_cta', JSON.stringify(pag_cta.items));
        console.log(pag_cta.items);
        
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {

            Swal.fire({
                title: '',
                text: 'Se registro correctamente',
                icon: 'success',
                timer: 2000,
                onClose: () => {
                    location.href = '/Compra/cta_x_pagar/list/';
                }
            }).then((result) => {

            });
        });
        console.log(pag_cta);
    });


});