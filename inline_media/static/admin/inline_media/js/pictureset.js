$(document).ready(function() {
    $("A[rel^='prettyPhoto']").prettyPhoto({social_tools:false});
    $("#content-related").css("height", $("#content-main").height()+110);
});
