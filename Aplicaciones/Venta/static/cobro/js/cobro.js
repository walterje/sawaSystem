var tbCtaXCb;
var cob_cta = {
    items: {
        cta_x_cobrar: '',
        fecha_cobro: '',
        montocob:0,
        caja:'',
        forma_cobro:'',
        saldo_actual: 0,
        vuelto: 0,
        efectivo:0,
        //monto_faltante: 0,
        cta:[],
    },
    
    calculate_monto_cob: function () {
        var saldo_actual = 0;
        var vuelto = 0;
        $.each(this.items.cta, function (pos, dict) {
            dict.pos = pos;
            dict.saldo_actual = dict.saldo - parseInt(dict.montocob);
            saldo_actual += dict.saldo_actual;
            console.log(dict.efectivo );
            dict.vuelto = dict.efectivo - parseInt(dict.montocob);
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
        this.calculate_monto_cob();
        tbCtaXCb=$('#tbCtaXCb').DataTable({
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
                {"data": "venta.cliente.cli"},
                {"data": "venta.fecha_venta"},
                {"data": "saldo"},
                {"data": "montocob"},
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
                        return '<input type="text" name="montocob" class="form-control form-control-sm" autocomplete="off" value="'+row.montocob+'">';
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

                $(row).find('input[name="montocob"]').TouchSpin({
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

    $('#fecha_cobro').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
     
    });
   
    
    // search cta_x_cobrar

    $('input[name="search"]').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_cta_x_cobrar',
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
            cob_cta.items.cta.length=0;
            ui.item.montocob = 0;
            ui.item.efectivo = 0;
            ui.item.vuelto = 0;
            cob_cta.items.cta_x_cobrar=(ui.item.id);
            ui.item.saldo_actual= ui.item.saldo;
            console.log(ui.item);
            cob_cta.add(ui.item);
            console.log(cob_cta.items);
            $(this).val('');
        }
    });
         //para limpiar el buscador
    $('.btnClearSearch').on('click', function () {
        $('input[name="search"]').val('').focus();
    }); 
     // event montocob

    $('#tbCtaXCb').on('change', 'input[name="montocob"]', function () {
        console.clear();
        var montocob = parseInt($(this).val());
        var tr = tbCtaXCb.cell($(this).closest('td, li')).index();
        if((cob_cta.items.cta[tr.row].venta.tipo_venta==0) && (montocob != cob_cta.items.cta[tr.row].monto_x_cobrar)){
            Swal.fire('Verifique el monto Cobrado')
        }
        
        cob_cta.items.cta[tr.row].montocob = montocob;
        console.log(cob_cta.items.fecha_cobro == cob_cta.items.cta[tr.row].venta.fecha_plazo);
        cob_cta.calculate_monto_cob();
        $('td:eq(4)', tbCtaXCb.row(tr.row).node()).html( agregarSeparadorMiles(cob_cta.items.cta[tr.row].saldo_actual.toFixed(0)));

    });
    //efectivo
 
     $('#tbCtaXCb').on('change', 'input[name="efectivo"]', function () {
        console.clear();
        var efectivo = parseInt($(this).val());
        var tr = tbCtaXCb.cell($(this).closest('td, li')).index();
        console.log(efectivo);
        console.log(cob_cta.items.cta[tr.row].montocob > efectivo);
        if( (cob_cta.items.cta[tr.row].montocob > efectivo)){
            Swal.fire('Verifique el monto del Efectivo');
            return false;
        }
       
        cob_cta.items.cta[tr.row].efectivo = efectivo;
        console.log(cob_cta.items.cta);
        cob_cta.calculate_monto_cob();
        $('td:eq(6)', tbCtaXCb.row(tr.row).node()).html( agregarSeparadorMiles(cob_cta.items.cta[tr.row].vuelto.toFixed(0)));
    });

    // para guardar mi orden  cobro
    $('form').on('submit', function (e) {
        e.preventDefault();
        console.log(cob_cta.items.cta[0]);
        if(cob_cta.items.cta.length === 0){
            message_error('Debe cargar un numero de cuenta');
            return false;
        }
        if(cob_cta.items.cta[0].montocob === 0){
            console.log('yes');
            Swal.fire('<p>Debe ingresar el monto que vas a cobrar</p>');
            return false;
        }
      
      
        
        console.log((cob_cta.items.cta[0].saldo));
        cob_cta.items.fecha_cobro = $('input[name="fecha_cobro"]').val();
        cob_cta.items.caja= $('select[name="caja"]').val();
        cob_cta.items.forma_cobro= $('select[name="forma_cobro"]').val();
        cob_cta.items.montocob=(cob_cta.items.cta[0].montocob);
        cob_cta.items.efectivo=(cob_cta.items.cta[0].efectivo);
        if((cob_cta.items.montocob != cob_cta.items.cta[0].saldo) && (cob_cta.items.fecha_cobro == cob_cta.items.cta[0].venta.fecha_plazo)){
            if(cob_cta.items.cta[0].venta.tipo_venta==1){
            Swal.fire('Su plazo vence hoy')
            return false;
            }
    
        }
        if(cob_cta.items.efectivo === 0){
            console.log('yes');
            Swal.fire('<p>Ingrese el monto del efectivo</p>');
            return false;
        }
        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('cob_cta', JSON.stringify(cob_cta.items));
        console.log(cob_cta.items);
        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {

            Swal.fire({
                title: '',
                text: 'Se registro correctamente',
                icon: 'success',
                timer: 2000,
                onClose: () => {
                    location.href = '/Venta/cta_x_cobrar/list/';
                }
            }).then((result) => {

            });
        });
        console.log(cob_cta);
    });


});