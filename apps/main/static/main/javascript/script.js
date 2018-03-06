$(document).ready(function(){
    console.log('anything')


    $('#showLoginForm').hide()

    $('#logInButton').click(function(event){
        event.preventDefault();
        $('#logInButton').hide()
        $('#showLoginForm').show()
    });    


});