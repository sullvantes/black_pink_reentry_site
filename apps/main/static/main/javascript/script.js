$(document).ready(function(){
    console.log('What the shitttes')


    $('#showLoginForm').hide()

    $('#logInButton').click(function(event){
        event.preventDefault();
        $('#logInButton').hide()
        $('#showLoginForm').show()
    });    


});