$(document).ready( function() {
    var counter = 1;
    $('.inputs-options a').click(function() {
        var name = "file_" + counter;
        counter += 1;
        var newinput = $("<input />").attr('type', 'file').attr('name', name);
        $('.inputs-container').append(newinput);
        return false;
    });
});
