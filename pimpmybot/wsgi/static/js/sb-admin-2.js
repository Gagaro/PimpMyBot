$(function() {

    $('#side-menu').metisMenu();

});

//Loads the correct sidebar on window load,
//collapses the sidebar on window resize.
// Sets the min-height of #page-wrapper to window size
$(function() {
    $(window).bind("load resize", function() {
        topOffset = 50;
        width = (this.window.innerWidth > 0) ? this.window.innerWidth : this.screen.width;
        if (width < 768) {
            $('div.navbar-collapse').addClass('collapse');
            topOffset = 100; // 2-row-menu
        } else {
            $('div.navbar-collapse').removeClass('collapse');
        }

        height = ((this.window.innerHeight > 0) ? this.window.innerHeight : this.screen.height) - 1;
        height = height - topOffset;
        if (height < 1) height = 1;
        if (height > topOffset) {
            $("#page-wrapper").css("min-height", (height) + "px");
        }
    });

    var url = window.location;
    var element = $('ul.nav a').filter(function() {
        return this.href == url || url.href.indexOf(this.href) == 0;
    }).addClass('active').parent().parent().addClass('in').parent();
    if (element.is('li')) {
        element.addClass('active');
    }
});

// Handle CSRF
var add_csrf_token = function(selector) {
    var csrf_token = $('body').attr('data-csrf');

    $(selector).find('form').prepend('<input type="hidden" name="_csrf_token" value="'+ csrf_token +'" />');
};

$(function() {
    var csrf_token = $('body').attr('data-csrf');

    add_csrf_token(document);

    $.ajaxSetup({
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CsrfToken', csrf_token);
        }
    });
});

/************************************************
 * MODAL
 ************************************************/

$('#modal').data('loading-html', $('#modal').html());

// Remove data so it will load new content.
$('body').on('hidden.bs.modal', '#modal', function () {
  $(this).removeData('bs.modal');
  $('#modal').html($('#modal').data('loading-html'));
});

$('body').on('loaded.bs.modal', '#modal', function () {
  /**
   ** Can be HTML or JSON body with the following attributes :
   **
   ** {
   **    "html": "Html to display in the modal",
   **    "redirect": "url to redirect to"
   **    "hide": true/false
   ** }
   **/

  try {
    var json = $(this).find('.modal-content').html();
    json = JSON.parse(json);

    $(this).find('.modal-content').html(json.html);
    if (json.redirect) {
      window.location = json.redirect;
    }
    if (json.hide) {
      $(this).modal('hide');
    }
  } catch (e) {/* No JSON */}

    add_csrf_token($(this));
});