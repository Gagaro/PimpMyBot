$(function() {
    // Init Dragula
    dragula({
        isContainer: function (el) {
            return el.classList.contains('dragula-draggable');
        }
    });

    // Enable or disable edit mode
    $('button#edit-dashboard').click(function() {
        $('button#edit-dashboard').hide();
        $('button#validate-dashboard').show();
        $('div#dashboard div.container').addClass('dragula-draggable');
    });
    $('button#validate-dashboard').click(function() {
        $('button#edit-dashboard').show();
        $('button#validate-dashboard').hide();
        $('div#dashboard div.container').removeClass('dragula-draggable');

        var dashboard = {
            'deactivated': $('div#deactivated .widget').map(function(){return $(this).attr("data-identifier");}).get(),
            'left': $('div#left .widget').map(function(){return $(this).attr("data-identifier");}).get(),
            'middle': $('div#middle .widget').map(function(){return $(this).attr("data-identifier");}).get(),
            'right': $('div#right .widget').map(function(){return $(this).attr("data-identifier");}).get(),
        };

        $.post(document.location.href, {data: JSON.stringify(dashboard)});
    });
});