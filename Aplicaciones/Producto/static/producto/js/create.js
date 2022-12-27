var select_tipo_producto;

$(function () {
    select_tipo_producto= $('select[name="tipo_producto"]');
       
    select_tipo_producto.on('change', function () {
        console.log(this.value==1);
       
        var container1 = $(this).parent().parent().parent().parent().parent().find('input[name="stock_minimo"]').parent();
        var container2 = $(this).parent().parent().parent().parent().parent().find('input[name="cant_stock"]').parent();
        var container3 = $(this).parent().parent().parent().parent().parent().find('input[name="precio_compra"]').parent();
        var container4 = $(this).parent().parent().parent().parent().parent().find('select[name="iva"]').parent();
        console.log($(this).parent());
        $(container1).hide();
        $(container2).hide();
        $(container3).hide();
        if (this.value==1) {
           $(container1).show();
           $(container2).show();
           $(container3).show();
           $(container4).show();
        }
        console.log(this);
    });
    if ($('input[name="action"]').val() === 'edit') {
        select_tipo_producto.trigger('change');
    }

});