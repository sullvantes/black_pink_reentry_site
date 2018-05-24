$(document).ready(function(){
    console.log('What the shitttes')


    $('#showLoginForm').hide()

    $('#logInButton').click(function(event){
        event.preventDefault();
        $('#logInButton').hide()
        $('#showLoginForm').show()
    });    

    $("#create-resource-list-title").click(function(){
        window.location = $(this).attr("data-href");
        return false;
    });

    $("#print-pdf-resource-list-title").click(function(){
        window.location = $(this).attr("data-href");
        return false;
    });

    $("#print-csv-resource-list-title").click(function(){
        window.location = $(this).attr("data-href");
        return false;
    });
});


jQuery(document).ready(function($) {
    $(".clickable-row").click(function() {
        window.location = $(this).data("href");
    });
});

