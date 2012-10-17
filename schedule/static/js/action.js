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
            $('.list_form tbody').append('<tr><td>'+data['payer']+'</td><td>'+data['description']+'</td><td>&euro; '+data['price']+'</td></tr>') 
        }
    });
})