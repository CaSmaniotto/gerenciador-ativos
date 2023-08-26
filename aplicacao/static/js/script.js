// table filter
$(document).ready(function(){
    $("#propInput").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#propTable tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});

$(document).ready(function(){
    $("#ativoInput").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#ativoTable tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});