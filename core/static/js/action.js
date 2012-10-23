$(function(){

    $('input:checkbox').change(function()
    {
        var toggle = $(this).is(':checked') ? 'on' : 'off'
        $.ajax('/schedule/' + $(this).val() + '/' + toggle + '/')
    })

    //$('#current_week').replaceWith('</tbody></table><table class="zoomed">' +  + '</table><table><tbody>')

    $( ".future_week span" ).draggable({revert: true, snap: true, snapModeType: 'outer'}).disableSelection();
    $( ".future_week span" ).droppable({
        drop: function( event, ui ) {
            $( this ).find( "p" ).html( "Dropped!" );
            $( "#switch_dialog" ).dialog({
                height: 140,
                modal: true,
                draggable: true,
                resizable: false,
            });
        }
    });

    // bind form and provide a simple callback function 
    $('.list_form').ajaxForm({ 
        // dataType identifies the expected content type of the server response 
        dataType:  'json', 
 
        // success identifies the function to invoke when the server response 
        // has been received 
        success:   function(data) { 
            $('.list_form .empty_table').hide()
            $('.list_form tbody').append('<tr><td>'+data['payer']+'</td><td>'+data['description']+'</td><td>&euro; '+data['price']+'</td></tr>') 
        }
    });
    
    $('.list_form select').select2();
    $('.list_form #eaters select').select2({
        width: '350px',
        formatSelection: function(object, container, query){
            return object.text + ' +  <input name="'+object.id+'_extra" style="width:20px" value="0" min="0" max="50" required="required" type="number" />'
        }
    });
    $('.list_form #eaters select').on("change", function(e) {
        $('input[type=number]').spinner();
    });

})
