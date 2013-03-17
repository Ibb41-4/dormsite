$(function(){

    $('input:checkbox').change(function()
    {
        var toggle = $(this).is(':checked') ? 'on' : 'off';
        $.ajax('/schedule/' + $(this).val() + '/' + toggle + '/');
    });

    //$('#current_week').replaceWith('</tbody></table><table class="zoomed">' +  + '</table><table><tbody>')

    $( ".switchable span" ).draggable({revert: true, revertDuration: 0, snap: true, snapModeType: 'outer'}).disableSelection();
    $( ".switchable span" ).droppable({
        drop: function( event, ui ) {
            //$("#replace_name").html($(this).html())

            var first = this;
            var id1 = first.id.substring(5);
            var other = ui.draggable.get(0);
            var id2 = other.id.substring(5);

            function swapNodes(a, b) {
                var aparent= a.parentNode;
                var asibling= a.nextSibling===b? a : a.nextSibling;
                b.parentNode.insertBefore(a, b);
                aparent.insertBefore(b, asibling);
            }

            $.ajax('/schedule/switch/' + id1 + '/' + id2 + '/', {
                success: function(text){
                    swapNodes(first.firstChild, other.firstChild);
                    alert(text);
                },
                error: function(a,b,text){
                    alert(text);
                }
            });
            /*

            $("#switch_dialog" ).dialog({
                height: 140,
                modal: true,
                draggable: true,
                resizable: false,
                buttons: [
                    { text: "Ok", click: function() {

                        $( this ).dialog( "close" );
                    }},
                    { text: "Annuleer", click: function() {
                        $( this ).dialog( "close" );
                    }}
                ]
            });*/
        }, activeClass: "highlight"
    });

    // bind form and provide a simple callback function
    $('.list_form').ajaxForm({
        // dataType identifies the expected content type of the server response
        dataType:  'json',

        // success identifies the function to invoke when the server response
        // has been received
        success:   function(data) {
            $('.list_form .empty_table').hide();
            $('.list_form tbody').append('<tr><td>'+data['payer']+'</td><td>'+data['description']+'</td><td>&euro; '+data['price']+'</td></tr>');
        }
    });

    //functions for eating list
    $('.list_form select').select2();
    $('.list_form #eaters select').select2({
        width: '350px',
        formatSelection: function(object, container, query){
            return object.text + ' +  <input name="'+object.id+'_extra" style="width:20px" value="0" min="0" max="50" required="required" type="number" />';
        }
    });
    $('.list_form #eaters select').on("change", function(e) {
        $('input[type=number]').spinner();
    });


    // relogin when user is changed
    $('#iplogin').change(function(){
        window.location.href = '/user/iplogin/' + $(this).val() + '/?next=' + window.location.pathname + window.location.search;
    });
});
