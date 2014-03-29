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