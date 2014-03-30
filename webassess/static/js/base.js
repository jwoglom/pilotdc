$(document).ready(function() {
    $(".left ul.nav > li[name]").click(function() {
        nav.go($(this).attr('name'));
    });
});
nav = {
    go: function(l) {
        location.href = '/'+l;
    }
}
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    crossDomain: false,
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", $.cookie("csrftoken"));
        }
    }
});