$(function(){

    $('input:checkbox').change(function()
    {
        var toggle = $(this).is(':checked') ? 'on' : 'off';
        $.ajax('/schedule/' + $(this).val() + '/' + toggle + '/');
    });

    //$('#current_week').replaceWith('</tbody></table><table class="zoomed">' +  + '</table><table><tbody>')

    $( ".switchable span" ).draggable({revert: true, revertDuration: 0, snap: true, snapModeType: 'outer'}).disableSelection();
    $( ".switchable span" ).droppable({
        drop: function( event, ui )
        {
            dragged = ui.draggable;
            replaced = $(this);

            $('#confirm-switch #replace_name1').text(dragged.text());
            $('#confirm-switch #replace_name2').text(replaced.text());

            $('#confirm-switch').modal();
            $('#confirm-switch .btn-primary').data('first', dragged.data('shift-id'));
            $('#confirm-switch .btn-primary').data('second', replaced.data('shift-id'));
        }, activeClass: "highlight"
    });

    $('#confirm-switch .btn-primary').click(function()
    {
        var self = $(this);
        self.button('loading');

        var id1 = $(this).data('first');
        var id2 = $(this).data('second');

        var show_result = function(text, success)
        {
            $('#confirm-switch').modal('hide');
            self.button('reset');
            $('.alert span').text(text);
            $('.alert').toggleClass('alert-success', success);
            $('.alert').toggleClass('alert-error', !success);
            $('.alert').show();
        };

        $.ajax('/schedule/switch/' + id1 + '/' + id2 + '/', {
            success: function(text){
                show_result(text, true);

                dragged = $('span[data-shift-id="'+id1+'"]');
                replaced = $('span[data-shift-id="'+id2+'"]');

                var temp = dragged.text();
                dragged.text(replaced.text());
                replaced.text(temp);
            },
            error: function(jqXHR){
                show_result(jqXHR.responseText, false);
            }
        });
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

    $('#div_id_goer').hide();
    $('#div_id_goer select').attr('disabled', 'disabled');
    $('.move_room .control-group').hide();
    $('.move_room').each(function(index, item) {
        goer = $('#div_id_goer option:selected').val();
        selected = $('option:selected', item);
        selected_string = goer == selected.val() ? 'checked="checked"' : '';
        $('.move_user', item).append(
            '<label class="radio"><input type="radio" ' +
            selected_string +
            ' name="goer" value="' +
            selected.val() +
            '"/><i class="icon-lock"></i>' +
            selected.text() +
            '</label>'
        );
    });
    $('.move_user').draggable({revert: true, revertDuration: 0, snap: true, snapModeType: 'inner', snapTolerance: '10', stack: ".move_user"}).disableSelection();
    $( ".move_room" ).droppable({
        drop: function(event, ui) {
            source = ui.draggable.parents('.move_room').first();
            target = $(this);

            dragged = ui.draggable;
            replaced = $('.ui-draggable', this);

            // Switch html
            source.append(replaced);
            target.append(dragged);

            //set selects
            $('select', source).val($('input', replaced).val());
            $('select', target).val($('input', dragged).val());
        }
    });
});
